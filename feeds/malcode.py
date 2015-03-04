#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2013, Neriberto C.Prado
#
# This file is part of HG - https://github.com/neriberto/hg
# See the file 'docs/LICENSE' for copying permission.

from hg.core.feeds import Feeds

class malcode(Feeds):

    Name = 'Malc0de'
    URL = 'http://malc0de.com/rss'

    def run(self, q):
        try:
            self.xml(q)
        except KeyboardInterrupt:
            pass
