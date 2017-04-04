#!/usr/bin/python
# -*- coding: utf-8 -*-

from hg.core.processors import Processors
import logging
import requests


class viper(Processors):
    '''
    Process submissions to Viper Framework
    '''

    Name = 'Viper'
    ADDURL = '%sfile/add'

    def not_exist(self, MD5, URL):
        '''
        Verify if a file already exists in Viper
        '''
        try:
            req = requests.post('%sfile/find' % URL, data={'md5': MD5})
            return req.status_code == 404
        except Exception as ex:
            logging.error('Viper:not_exist %s', ex)
            return False
