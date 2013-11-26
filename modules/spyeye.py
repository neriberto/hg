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
        try:
            r = requests.get("https://spyeyetracker.abuse.ch/monitor.php?urlfeed=binaryurls")
            content = r.content
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
        except Exception:
            # Sometimes Spyeye give us 502 status code :)
            pass
