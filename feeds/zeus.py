#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2013, Neriberto C.Prado
#
# This file is part of HG - https://github.com/neriberto/hg
# See the file 'docs/LICENSE' for copying permission.

from hg.core.feeds import Feeds
from lxml import etree


class zeus(Feeds):

    Name = 'Zeus'
    URL = 'https://zeustracker.abuse.ch/monitor.php?urlfeed=binaries'

    def run(self, q):
        try:
            self.xml(q)
        except KeyboardInterrupt:
            pass
        except Exception as ex:
            self.print_error(ex, content)
