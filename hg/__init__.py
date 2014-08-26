# -*- coding: utf-8 -*-
#

import ConfigParser
import os
import fnmatch
import hashlib
import logging
import magic
import Queue
import time
import threading
import requests
import sys
from pprint import pprint

class hg(object):

    _Config = {}
    _Processors = []
    _Feeds = []
    _Fila = Queue.Queue()
    _End_Process = False
    _NUM_CONCURRENT_DOWNLOADS = 2

    def __init__(self, downloads=2):
        self._NUM_CONCURRENT_DOWNLOADS = downloads
        Path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../")
        self._Processors = self.LoadModules(Path, "processors")
        self._Feeds = self.LoadModules(Path, "feeds")
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            stream=sys.stdout)
        fconf = os.path.join(Path, "conf/hg.conf")
        if os.path.exists(fconf):
            cfg = ConfigParser.ConfigParser()
            cfg.read(fconf)

            VX = {}
            VX["Enabled"]= cfg.get('vxcage', 'enabled')
            VX["connection"] = cfg.get('vxcage', 'connection');

            Viper = {}
            Viper["Enabled"] = cfg.get('viper', 'enabled')
            Viper["connection"] = cfg.get('viper', 'connection');

            Cuckoo = {}
            Cuckoo["Enabled"]= cfg.get('cuckoo', 'enabled')
            Cuckoo["connection"] = cfg.get('cuckoo', 'connection');

            Mongo = {}
            Mongo["Enabled"]= cfg.get('mongodb', 'enabled')
            Mongo["host"] = cfg.get('mongodb', 'host');
            Mongo["port"] = cfg.get('mongodb', 'port');

            self._Config["VxCage"] = VX
            self._Config["Cuckoo"] = Cuckoo
            self._Config["Mongo"] = Mongo
            self._Config["Viper"] = Viper

        logging.info("Initializing HG")

    def LoadModules(self, Root, Directory):
        Modules = []
        Walk_In = os.path.join(Root, Directory)
        for arg, dirname, names in os.walk(Walk_In):
            for name in fnmatch.filter(names, "*.py"):
                if name != "__init__.py":
                    name = "%s.%s" % (Directory, name.split(".py")[0])
                    processor = __import__(name, globals(), locals(), [''])
                    components = name.split(".")[1:]
                    for com in components:
                        class_ = getattr(processor, com)
                        Modules.append(class_())
        return Modules

    def SaveFile(self, data):
        path = os.path.join("/tmp/", data["filename"])
        fp = open(path, "wb")
        fp.write(data["content"])
        fp.close()
        return path

    def GetFileType(self, data):
        filetype = None
        try:
            # using python-magic from apt-get(Ubuntu)
            ms = magic.open(magic.MAGIC_MIME)
            ms.load()
            filetype = ms.buffer(data)
        except:
            try:
                # from pip install libmagic, python-magic
                filetype = magic.Magic(mime=True).from_buffer(data)
            except Exception as e:
                logging.error(e)
                self._End_Process = True

        return filetype.split(";")[0]


    def Fetch(self, URL):
        try:
            headers = {'User-Agent':'Mozilla/5.0'}
            re = requests.get(URL,
                              allow_redirects=True,
                              timeout=100,
                              headers=headers)
            if re.status_code == 200:
                UseDisp = False
                for item in re.headers:
                    if item.lower() == "content-disposition":
                        UseDisp = True
                if not UseDisp:
                    filename = URL.split('/')[-1].split('#')[0].split('?')[0]
                    if filename == None:
                        filename = URL.split('/')
                else:
                    Disposition = re.headers['Content-Disposition']
                    try:
                        filename = Disposition.split('filename=')[1].split('"')[1]
                    except Exception:
                        filename = Disposition.split('filename=')[1].split('"')[0]
                return dict({"filename":filename,
                             "content": re.content,
                             "status_code": re.status_code})
            else:
                return dict({"filename": None,
                             "content": None,
                             "status_code": re.status_code})
        except Exception, e:
            return dict({"filename": None,
                         "content": None,
                         "status_code": "0"}) # 0 for timeout
        except KeyboardInterrupt:
            pass

    def Downloader(self):
        while not self._End_Process:
            try:
                url = self._Fila.get(True, 5)
            except Queue.empty:
                continue
            data = self.Fetch(url)
            message = "Status Code: "+str(data["status_code"])+" URL: "+ url[0:50]
            if data["status_code"] != 200:
                logging.error(message)
            else:
                logging.info(message)

            if data['content'] != None:
                fpath = self.SaveFile(data)
                ftype = self.GetFileType(data['content'])
                if (os.path.getsize(fpath) > 0):
                    MD5 = hashlib.md5(data['content']).hexdigest()
                    for proc in self._Processors:
                        proc.run(self._Config, MD5, fpath, ftype)
                os.remove(fpath)
            data = None
            self._Fila.task_done()

    def run(self):
        threads = []

        logging.info("Initializing Downloaders")
        for unused_index in range(self._NUM_CONCURRENT_DOWNLOADS):
            thread = threading.Thread(target=self.Downloader)
            thread.daemon = True
            thread.start()
            threads.append(thread)

        while not self._End_Process:
            try:
                if self._Fila.qsize() > 300:
                    logging.info("Too many files to retrieve, waiting")
                    time.sleep(30)
                    continue
                for feed in self._Feeds:
                    try:
                        feed.run(self._Fila)
                    except Exception as e:
                        logging.error("Feed with errors: %s", feed.Name)
                        logging.error(e)
                        sys.exit(-1)
                logging.info("Feeds retrieved, waiting")
                time.sleep(30)
            except KeyboardInterrupt:
                logging.info("Shutdown HG")
                self._End_Process = True
