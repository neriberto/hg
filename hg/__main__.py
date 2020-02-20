"""HG - Hazardous Garbage, a malware collector."""

from os.path import dirname
from sys import path

import hg

if __package__ == '':
    path.insert(0, dirname(__file__))


if __name__ == '__main__':
    hg.cli()
