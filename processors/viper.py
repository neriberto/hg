# Copyright (c) 2013, Neriberto C.Prado
#
# This file is part of HG - https://github.com/neriberto/hg
# See the file 'docs/LICENSE' for copying permission.

# -*- coding: utf-8 -*-

import os
import requests

class viper (object):

    TYPES = []

    def __init__(self):
        self.TYPES.append("application/x-dosexec")
        self.TYPES.append("application/x-executable")
        self.TYPES.append("application/pdf")
        self.TYPES.append("application/msword")
        self.TYPES.append("application/octet-stream")

    def run(self, CONFIG, MD5, FULLPATH, FILETYPE):
        try:
            if CONFIG['Viper']['Enabled'] == "yes":
                if FILETYPE in self.TYPES:
                    if self.not_exist(MD5, CONFIG['Viper']['connection']):
                        return self.add(CONFIG["Viper"]['connection'], FULLPATH)
        except Exception, e:
            print "Viper:run %s" % (e)

    def not_exist(self, MD5, URL):
        try:
            Data = {'md5': MD5}
            r = requests.post("%sfile/find" % URL, data=Data)
            return (r.status_code == 404)
        except Exception, e:
            print "Viper:not_exist %s" % (e)
            return False

    def add(self, URL, fullpath):
        try:
            Files = {'file': (os.path.basename(fullpath), open(fullpath, 'rb'))}
            r = requests.post("%sfile/add" % URL, files=Files)
            return (r.status_code == 200)
        except Exception, e:
            print "Viper:add %s" % (e)
            return False