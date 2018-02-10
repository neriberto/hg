#!/usr/bin/python
# -*- coding: utf-8 -*-

import feedparser
import logging
import re
import urllib2


class Feeds(object):

    Name = None
    URL = None

    def __init(self):
        logging.info('Reading feed %s in URL %s', self.Name, self.URL)

    def Download(self, URL):
        """Execute download from a URL."""
        try:
            head = {'User-agent': 'Mozilla/5.0 (X11; U; Linux i686)'}
            r = urllib2.Request(URL, headers=head)
            return urllib2.urlopen(r)
        except Exception as e:
            logging.error('Failure, %s' % e)
            return None

    def process_xml_list_desc(self, response):
        for entry in feedparser.parse(response).entries:
            desc = entry.description
            url = desc.split(' ')[1].rstrip(',')
            if url == '':
                continue
            if url == '-':
                url = desc.split(' ')[4].rstrip(',')
            url = re.sub('&amp;', '&', url)
            if not re.match('http', url):
                url = 'http://' + url
            yield url

    def xml(self, q):
        content = self.Download(self.URL)
        for url in self.process_xml_list_desc(content):
            q.put(url, True, 5)
