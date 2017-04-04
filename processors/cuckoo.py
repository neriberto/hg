#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2013, Neriberto C.Prado
#
# This file is part of HG - https://github.com/neriberto/hg
# See the file 'docs/LICENSE' for copying permission.

from hg.core.processors import Processors
import logging
import requests


class cuckoo(Processors):

    Name = 'Cuckoo'
    ADDURL = '%stasks/create/file'

    def not_exist(self, MD5, URL):
        try:
            Data = {'md5': MD5}
            URL_PATH = '%sfiles/view/md5/%s' % (URL, MD5)
            r = requests.get(URL_PATH, data=Data)
            return r.status_code == 404
        except Exception as e:
            logging.error('Cuckoo:not_exist %s' % e)
            return False
