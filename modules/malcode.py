# Copyright (c) 2013, Neriberto C.Prado
#
# This file is part of HG - https://github.com/neriberto/hg
# See the file 'docs/LICENSE' for copying permission.

# -*- coding: utf-8 -*-

import requests
from xml.dom.minidom import parseString

class malcode (object):

    def run(self):
        URLS = []
        # Download list from malc0de
        content = self.Download("http://malc0de.com/rss")
        if content != None:
            bk = content.replace("\n", "")
            dom = parseString(bk.encode("utf-8"))
            for node in dom.getElementsByTagName("description"):
                # extract the URLs
                line = node.toxml().replace("<description>", "")
                info = line.replace("</description", "")
                try:
                    URLS.append("http://" + info.split(',')[0].split(':')[1][1:])
                except:
                    pass
            return URLS
        else:
            return None

    def Download(self, URL):
        '''
        :description : Execute download from a URL
        '''
        try:
            r = requests.get(URL)
            return r.content
        except Exception, e:
            print "Failure, %s" % e
            return None
