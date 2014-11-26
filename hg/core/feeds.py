#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import urllib2
from lxml import etree


class Feeds(object):

    def Download(self, URL):
        '''
        :description : Execute download from a URL
        '''

        try:
            head = {'User-agent': 'Mozilla/5.0 (X11; U; Linux i686)'}
            r = urllib2.Request(URL, headers=head)
            return urllib2.urlopen(r)
        except Exception, e:
            logging.error('Failure, %s' % e)
            return None

    def print_error(self, ex, buff):
        logging.error(ex)
        print " "
        print buff
