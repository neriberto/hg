#!/usr/bin/env python
#
# Copyright (c) 2013, Neriberto C.Prado
#
# This file is part of HG - https://github.com/neriberto/hg
# See the file 'docs/LICENSE' for copying permission.

# -*- coding: utf-8 -*-

import ConfigParser
import datetime
import fnmatch
import hashlib
import magic
import os
import requests
import sys

def getConfig(directory):
    '''
    Read config file and return VxCage URL
    '''
    fconf = os.path.join(directory, "conf/hg.conf")
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

        Config = {}
        Config["VxCage"] = VX
        Config["Cuckoo"] = Cuckoo
    	Config["Mongo"] = Mongo
        Config["Viper"] = Viper

        return Config
    else:
        sys.stderr.write("Cannot found config file %s\n" % fconf)
        return None

def getModules(directory):
    '''
    Loads all modules of Malware Repository
    '''
    Modules = []
    WALK_IN = os.path.join(directory, 'modules')
    for arg, dirname, names in os.walk(WALK_IN):
        for name in fnmatch.filter(names, "*.py"):
            if name != "__init__.py":
                name = "modules.%s" % name.split(".py")[0]
                module = __import__(name, globals(), locals(), [''])
                components = name.split('.')
                for comp in components[1:]:
                    class_ = getattr(module, comp)
                    Modules.append(class_())
    return Modules

def getProcessors(directory):
    '''
    Loads all processor for Malware Repository
    '''
    Processors = []
    WALK_IN = os.path.join(directory, 'processors')
    for arg, dirname, names in os.walk(WALK_IN):
        for name in fnmatch.filter(names, "*.py"):
            if name != "__init__.py":
                name = "processors.%s" % name.split(".py")[0]
                processor = __import__(name, globals(), locals(), [''])
                components = name.split('.')
                for comp in components[1:]:
                    class_ = getattr(processor, comp)
                    Processors.append(class_())
    return Processors

def getSample(URL):
    '''
    Download file from a URL
    '''
    try:
        headers = {'User-Agent':'Mozilla/5.0'}
        re = requests.get(URL, allow_redirects=True, timeout=100, headers=headers)
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
        print "getSample: %s" % (e)
        return dict({"filename": None,
                     "content": None,
                     "status_code": "0"}) # 0 for timeout

def saveFile(data):
    fullpath = os.path.join('/tmp/', data['filename'])
    fp = open(fullpath, "wb")
    fp.write(data['content'])
    fp.close()
    return fullpath

def getType(data):
    try:
        ms = magic.open(magic.MAGIC_MIME)
        ms.load()
        filetype = ms.buffer(data)
        return filetype.split(";")[0]
    except:
        try:
            filetype = magic.from_buffer(data)
            return filetype.split(";")[0]
        except Exception, e:
            print "getType %s" % (e)
            sys.exit(-1)

def getURLS(DIRECTORY, CONFIG, URLS):
    '''
    Works on a list of URLs
    '''
    print "URLs Encontradas: %s" % len(URLS)
    Processors = getProcessors(DIRECTORY)
    count = 0
    for url in URLS:
        count += 1
        data = getSample(url)
        print "%04d - [%s] - Status Code:%s\t%s" %  (
            count,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data['status_code'],
            url[0:50])
        try:
            if data['content'] != None:
                fullpath = saveFile(data)
                filetype = getType(data['content'])
                if (os.path.getsize(fullpath) > 0):
                    md5 = hashlib.md5(data['content']).hexdigest()
                    for processor in Processors:
                        processor.run(CONFIG, md5, fullpath, filetype)
                os.remove(fullpath)
            # clean memory
            data = None
        except Exception, e:
            # Failure in download, go to next 
            #print "getURLS: %s - %s" % (url, e)
            pass

def main():
    '''
    Main Procedure
    '''
    URLS = []
    REPORT = []
    INSTALLDIR = os.path.dirname(os.path.realpath(__file__))
    Config = getConfig(INSTALLDIR)
    mods = getModules(INSTALLDIR)
    for mod in mods:
        lista = mod.run()
        if lista != None:
            URLS += lista
        REPORT.append({"Source":mod.Name,"URL":mod.URL,"URLS":lista})

    getURLS(INSTALLDIR, Config, URLS)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    except SystemExit:
        pass
