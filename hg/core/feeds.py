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
        '''
        :description : Execute download from a URL
        '''

        try:
            head = {'User-agent': 'Mozilla/5.0 (X11; U; Linux i686)'}
            r = urllib2.Request(URL, headers=head)
            return urllib2.urlopen(r)
        except Exception as e:
            logging.error('Failure, %s' % e)
            return None

    def print_error(self, ex, buff):
        logging.error(ex)
        print(" ")
        print(buff)

    def process_xml_list_desc(self, response):
        feed = feedparser.parse(response)
        urls = set()

        for entry in feed.entries:
            desc = entry.description
            url = desc.split(' ')[1].rstrip(',')
            if url == '':
                continue
            if url == '-':
                url = desc.split(' ')[4].rstrip(',')
            url = re.sub('&amp;', '&', url)
            if not re.match('http', url):
                url = 'http://' + url
            urls.add(url)

        return urls

    def xml(self, q):
        content = self.Download(self.URL)
        urls = self.process_xml_list_desc(content)
        for url in urls:
            q.put(url, True, 5)
