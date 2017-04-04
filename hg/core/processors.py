#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import requests


class Processors(object):

    Name = ""
    ADDURL = '%stasks/create/file'
    TYPES = []

    def __init__(self):
        self.TYPES.append('application/x-dosexec')
        self.TYPES.append('application/x-executable')
        self.TYPES.append('application/pdf')
        self.TYPES.append('application/msword')
        self.TYPES.append('application/octect-stream')
        logging.info('Processor %s ready', self.Name)

    def run(self, CONFIG, MD5, FULLPATH, FILETYPE):
        try:
            if CONFIG[self.Name]['Enabled'] == 'yes':
                if FILETYPE in self.TYPES:
                    connection = CONFIG[self.Name]['connection']
                    # if self.not_exist(MD5, connection):
                    return self.add(connection, FULLPATH)
        except Exception as ex:
            logging.error('%s:run %s' % self.Name, ex)

    def add(self, URL, fullpath):
        logging.info('Submitting file %s to %s', fullpath, URL)
        try:
            arquivo = os.path.basename(fullpath)
            my_files = {'file': (arquivo, open(fullpath, 'rb'))}
            req = requests.post(self.format_url(URL), files=my_files)
            return req.status_code == 200
        except Exception as ex:
            logging.error('%s:add %s', self.Name, ex)
            return False

    def format_url(self, URL):
        return self.ADDURL % URL

    def not_exist(self, MD5, connection):
        return None
