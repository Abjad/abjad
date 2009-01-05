#! /usr/bin/env python


### TODO - replace os.system( ) with the Python 2.4 subprocess module

import os
CURDIR = os.path.abspath(os.curdir)

from abjad.cfg.cfg import ABJADPATH

ABJADDOCSCR = os.sep.join([ABJADPATH, 'documentation', 'scr'])
raw_parser = os.sep.join([ABJADDOCSCR, 'raw_parser.py'])
raw_file = os.sep.join([CURDIR, 'text.raw'])
wrap_html = os.sep.join([ABJADDOCSCR, 'wrap_html.py'])
html_file = os.sep.join([CURDIR, 'text.html'])
os.system('clear')
os.system('%s %s' % (raw_parser, raw_file))
os.system('%s -f %s' % (wrap_html, html_file))
