# Copyright (c) 2013, Neriberto C.Prado
#
# This file is part of HG - https://github.com/neriberto/hg
# See the file 'docs/LICENSE' for copying permission.


from hg.core.feeds import Feeds
from lxml import etree

class malcode (Feeds):

    Name = "Malc0de"
    URL = "http://malc0de.com/"

    def run(self):
        URLS = []
        # Download list from malc0de
        content = self.Download("http://malc0de.com/rss/")
        if content != None:
            children = ["title", "description", "link"]
            main_node = "item"

            tree = etree.parse(content)
            for item in tree.findall("//%s" % main_node):
                dict = {}
                for field in children:
                    dict[field] = item.findtext(field)
                URLS.append("http://%s" % dict['description'].split(" ")[1][:-1])
            return URLS
        else:
            return None
