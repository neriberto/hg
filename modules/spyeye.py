# Copyright (c) 2013, Neriberto C.Prado
#
# This file is part of HG - https://github.com/neriberto/hg
# See the file 'docs/LICENSE' for copying permission.

# -*- coding: utf-8 -*-

from xml.dom.minidom import parseString
import requests

class spyeye(object):

    def run(self):
        URLS = []
        # Download list from Zeus tracker
        content = self.Download("https://spyeyetracker.abuse.ch/monitor.php?urlfeed=binaryurls")
        if content != None:
            bk = content.replace("\n","")
            dom = parseString(bk.encode("utf-8"))
            for node in dom.getElementsByTagName("title"):
                # extract the URLs
                line = node.toxml().replace("<title>", "")
                info = line.replace("</title>", "")
                try:
                    URLS.append("http://" + info.split(',')[0].split(':')[0].split(' ')[0])
                except:
                    pass
        URLS.pop(0)
        return URLS

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
