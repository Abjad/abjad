from abjad.cfg.cfg import ABJADPATH
import os


def make_html_docs():

   # print greeting
   print 'Now building the HTML docs ...'
   print ''

   # change to docs directory because makefile lives there
   docs_directory = os.path.join(ABJADPATH, 'docs')
   os.chdir(docs_directory)

   # make html docs
   os.system('make html')
