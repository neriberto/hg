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
            if self.not_exist(MD5, CONFIG['VxCage']['connection']):
                return self.add(CONFIG["VxCage"]['connection'], FULLPATH)

    def not_exist(self, MD5, URL):
        Data = {'md5': MD5}
        try:
            r = requests.post("%smalware/find" % URL, data=Data)
            return (r.status_code == 404)
        except:
            return False

    def add(self, URL, fullpath):
        Files = {'file': (os.path.basename(fullpath), open(fullpath, 'rb'))}
        r = requests.post("%smalware/add" % URL, files=Files)
        # Returns 200 upload sucessfull, so remove
        return (r.status_code == 200)
