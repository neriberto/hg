#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import requests


class Processors(object):

    Name = ""
    ADDURL = '%stasks/create/file'
    __TYPES = []

    def __init(self):
        self.TYPES.append('application/x-dosexec')
        self.TYPES.append('application/x-executable')
        self.TYPES.append('application/pdf')
        self.TYPES.append('application/msword')
        self.TYPES.append('application/octect-stream')

    def run(self, CONFIG, MD5, FULLPATH, FILETYPE):
        try:
            if CONFIG[self.Name]['Enabled'] == 'yes':
                if FILETYPE in self.TYPES:
                    connection = CONFIG[self.Name]['connection']
                    if self.not_exist(MD5, connection):
                        return self.add(connection, FULLPATH)
        except Exception as ex:
            logging.error('%s:run %s' % self.Name, ex)

    def add(self, URL, fullpath):
        try:
            arquivo = os.path.basename(fullpath)
            Files = {'file': (arquivo, open(fullpath, 'rb'))}
            r = requests.post(self.format_url(URL), files=Files)
            return r.status_code == 200
        except Exception as ex:
            logging.error('%s:add %s', self.Name, ex)
            return False

    def format_url(self, URL):
        return self.ADDURL % URL
