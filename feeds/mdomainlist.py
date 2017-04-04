#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2013, Neriberto C.Prado
#
# This file is part of HG - https://github.com/neriberto/hg
# See the file 'docs/LICENSE' for copying permission.


from hg.core.feeds import Feeds


class mdomainlist(Feeds):

    Name = 'Malware Domain List'
    URL = 'http://www.malwaredomainlist.com/hostslist/mdl.xml'

    def run(self, q):
        try:
            self.xml(q)
        except KeyboardInterrupt:
            pass
