# Copyright (c) 2013, Neriberto C.Prado
#
# This file is part of HG - https://github.com/neriberto/hg
# See the file 'docs/LICENSE' for copying permission.

# -*- coding: utf-8 -*-

from hg.core.feeds import Feeds
from lxml import etree

class mblacklist(Feeds):

    Name = "Malware Blacklist"
    URL = "http://www.malwareblacklist.com/mbl.xml"

    def run(self, q):
        try:
            content = self.Download(self.URL)
            if content != None:
                children = ["title", "link", "description", "guid"]
                main_node = "item"

                tree = etree.parse(content)
                for item in tree.findall("//%s" % main_node):
                    dic = {}
                    for field in children:
                        if field == "description":
                            dic[field] = item.findtext(field)
                            url = dic['description'].split(" ")[1][:-1]
                            q.put(url, True, 5)

        except KeyboardInterrupt:
            pass
