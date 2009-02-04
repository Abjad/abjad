#! /usr/bin/env python

from abjad.cfg.cfg import ABJADPATH
import os
import subprocess
import sys


CURDIR = os.path.abspath(os.curdir)
ABJADDOCSCR = os.sep.join([ABJADPATH, 'documentation', 'scr'])
raw_parser = os.sep.join([ABJADDOCSCR, 'raw_parser.py'])
raw_file = os.sep.join([CURDIR, 'text.raw'])
wrap_html = os.sep.join([ABJADDOCSCR, 'wrap_html.py'])
html_file = os.sep.join([CURDIR, 'text.html'])
p = subprocess.Popen('%s %s' % (raw_parser, raw_file), 
   shell = True, stdout = sys.stdout)
p.communicate( )
p = subprocess.Popen('%s -f %s' % (wrap_html, html_file), shell = True)
p.communicate( )
