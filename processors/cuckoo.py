#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2013, Neriberto C.Prado
#
# This file is part of HG - https://github.com/neriberto/hg
# See the file 'docs/LICENSE' for copying permission.

import logging
import os
import requests


class cuckoo(object):

    TYPES = []

    def __init__(self):
        self.TYPES.append('application/x-dosexec')
        self.TYPES.append('application/x-executable')
        self.TYPES.append('application/pdf')
        self.TYPES.append('application/msword')
        self.TYPES.append('application/octet-stream')

    def run(self, CONFIG, MD5, FULLPATH, FILETYPE):

        try:
            if CONFIG['Cuckoo']['Enabled'] == 'yes':
                if FILETYPE in self.TYPES:
                    cuckoo_conn = CONFIG['Cuckoo']['connection']
                    if self.not_exist(MD5, cuckoo_conn):
                        return self.add(cuckoo_conn, FULLPATH)
        except Exception as e:
            logging.error('Cuckoo:run %s' % e)
            return False

    def not_exist(self, MD5, URL):
        try:
            Data = {'md5': MD5}
            URL_PATH = '%sfiles/view/md5/%s' % (URL, MD5)
            r = requests.get(URL_PATH, data=Data)
            return r.status_code == 404
        except Exception, e:
            logging.error('Cuckoo:not_exist %s' % e)
            return False

    def add(self, URL, fullpath):
        try:
            Files = {'file': (os.path.basename(fullpath),
                     open(fullpath, 'rb'))}
            URL_PATH = '%stasks/create/file' % URL
            r = requests.post(URL_PATH, files=Files)
            return r.status_code == 200
        except Exception, e:
            logging.error('Cuckoo:add %s' % e)
            return False
