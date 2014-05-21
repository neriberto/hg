# Copyright (c) 2013, Neriberto C.Prado
#
# This file is part of HG - https://github.com/neriberto/hg
# See the file 'docs/LICENSE' for copying permission.

# -*- coding: utf-8 -*-

from hg.core.feeds import Feeds
from lxml import etree

class mdomainlist(Feeds):

    Name = "Malware Domain List"
    URL = "http://www.malwaredomainlist.com/hostslist/mdl.xml"

    def run(self):
        URLS = []
        content = self.Download(self.URL)
        if content != None:
            children = ["title", "link", "description", "guid"]
            main_node = "item"

            tree = etree.parse(content)
            for item in tree.findall("//%s" % main_node):
                dict = {}
                for field in children:
                    dict[field] = item.findtext(field)
                URLS.append(dict['description'].split(" ")[1][:-1])
            return URLS
        else:
            return None
