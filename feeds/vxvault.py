# Copyright (c) 2013, Neriberto C.Prado
#
# This file is part of HG - https://github.com/neriberto/hg
# See the file 'docs/LICENSE' for copying permission.


from hg.core.feeds import Feeds
from lxml import etree

class vxvault (Feeds):

    Name = "VxVault"
    URL = "http://vxvault.siri-urz.net/URL_List.php"

    def run(self):
        URLS = []
        content = self.Download(self.URL)
        if content != None:
            URLS = content.read().split("\r\n")
            URLS.pop(3)
            URLS.pop(2)
            URLS.pop(1)
            URLS.pop(0)
            return URLS
        else:
            return None
