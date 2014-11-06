#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from hg import hg


def main():
    HG = hg(10)
    HG.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    except SystemExit:
        pass
