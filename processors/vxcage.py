# Copyright (c) 2013, Neriberto C.Prado
#
# This file is part of HG - https://github.com/neriberto/hg
# See the file 'docs/LICENSE' for copying permission.

# -*- coding: utf-8 -*-

import os
import requests

class vxcage (object):

    def run(self, CONFIG, MD5, FULLPATH):
        if CONFIG['VxCage']['Enabled'] == "yes":
            if self.exist(MD5, CONFIG['VxCage']['connection']) == 404:
                self.add(CONFIG["VxCage"]['connection'], FULLPATH)

    def exist(self, MD5, URL):
        Data = {'md5': MD5}
        try:
            r = requests.post("%smalware/find" % URL, data=Data)
            return r.status_code
        except:
            return -1

    def add(self, URL, fullpath):
        Uploaded = False
        Count = 0
        # Check first if the file is not empty
        if (os.path.getsize(fullpath) > 0):
            Files = {'file': (os.path.basename(fullpath), open(fullpath, 'rb'))}
            # Try 3 times if receive upload error
            while (not Uploaded) or (Count == 3):
                r = requests.post("%smalware/add" % URL, files=Files)
                # Returns 200 upload sucessfull, so remove
                if r.status_code == 200:
                    Uploaded = True
                else:
                    Count += 1
                if Count == 3:
                    print "Failure in send to VxCage in %s" % URL
