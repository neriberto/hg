#!/usr/bin/env python
#
# Copyright (c) 2013, Neriberto C.Prado
#
# This file is part of HG - https://github.com/neriberto/hg
# See the file 'docs/LICENSE' for copying permission.

# -*- coding: utf-8 -*-

import ConfigParser
import fnmatch
import hashlib
import os.path
import requests
import sys

def getConfig():
    '''
    Read config file and return VxCage URL
    '''
    fconf = "conf/hg.conf"
    if os.path.exists(fconf):
        cfg = ConfigParser.ConfigParser()
        cfg.read(fconf)
        IP = cfg.get('vxcage', 'ip');
        PORT = cfg.get('vxcage', 'port');
        return "http://%s:%s/" % (IP, PORT)
    else:
        sys.stderr.write("Cannot found config file %s\n" % fconf)
        return None

def getModules():
    '''
    Loads all modules of Malware Repository
    '''
    Modules = []
    for arg, dirname, names in os.walk('modules'):
        for name in fnmatch.filter(names, "*.py"):
            if name != "__init__.py":
                name = "modules.%s" % name.split(".py")[0]
                module = __import__(name, globals(), locals(), [''])
                components = name.split('.')
                for comp in components[1:]:
                    class_ = getattr(module, comp)
                    Modules.append(class_())
    return Modules

def getSample(URL):
    '''
    Download file from a URL
    '''
    re = requests.get(URL, allow_redirects=True, timeout=300)
    if re.status_code == 200:
        if re.headers['Content-Disposition'] == None:
            filename = URL.split('/')[-1].split('#')[0].split('?')[0]
            if filename == None:
                filename = URL.split('/')
        else:
            Disposition = re.headers['Content-Disposition']
            try:
                filename = Disposition.split('=')[1].split('"')[1]
            except:
                filename = Disposition.split('=')[1].split('"')[0]
        try:
            return dict({"filename": filename, "content": re.content})
        except Exception, e:
            print "getSample %s" % e
            return dict({"filename": None, "content": None})
    else:
        print "Status Code %d" % re.status_code
        return dict({"filename": None, "content": None})

def doUpload(URL, fullpath):
    '''
    Send the sample in fullpath to VxCage
    '''
    # TODO: Execute file scanners to verify is the Zip File is a JAR or APK
    # and sends the real file type as a TAG to VxCage
    Uploaded = False
    Count = 0
    # TODO: Check first if the file is not empty
    if (os.path.getsize(fullpath) > 0):
        Files = {'file': (os.path.basename(fullpath), open(fullpath, 'rb'))}
        # Try 3 times if receive upload error
        while (not Uploaded) or (Count == 3):
            r = requests.post("%smalware/add" % URL, files=Files)
            # Returns 200 upload sucessfull, so remove
            if r.status_code == 200:
                os.remove(fullpath)
                Uploaded = True
            else:
                Count += 1
        if Count == 3:
            print "Failure in send to VxCage in %s" % URL
            sys.exit(-1)


def getURLS(URL, URLS):
    '''
    Works on a list of URLs
    '''
    print "URLs Encontradas: %s" % len(URLS)

    count = 0
    for url in URLS:
        count += 1
        print "%d - %s" %  (count, url[0:50])
        try:
            data = getSample(url)
            if data['content'] != None:
                md5 = hashlib.md5(data['content']).hexdigest()
                try:
                    Data = {'md5': md5}
                    r = requests.post('%smalware/find' % URL, data=Data)
                except:
                    print "Failure to query VxCage, exiting"
                    sys.exit(-1)
                # Returns 404 file don't exist in VxCage
                if r.status_code == 404:
                    # save in temp to upload to VxCage
                    fullpath = os.path.join('/tmp/', data['filename'])
                    fp = open(fullpath, "wb")
                    fp.write(data['content'])
                    fp.close()
                    # Send to VxCage Server
                    doUpload(URL, fullpath)
                else:
                    # File already downloaded
                    pass
            else:
                # Empty content after download
                pass
            # clean memory
            data = None
        except Exception:
            # Failure to download, go to next 
            pass

def main():
    '''
    Main Procedure
    '''
    URLS = []
    VxCageAddress = getConfig()
    mods = getModules()
    for mod in mods:
        lista = mod.run()
        if lista != None:
            URLS += lista

    getURLS(VxCageAddress, URLS)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    except SystemExit:
        pass
