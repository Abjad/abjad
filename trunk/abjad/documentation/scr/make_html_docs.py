from abjad.cfg.cfg import ABJADPATH
import os


def make_html_docs( ):

   ## print greeting
   print 'Now building the HTML docs ...'
   print ''

   ## change to documentation directory because makefile lives there
   documentation_directory = os.path.join(ABJADPATH, 'documentation')
   os.chdir(documentation_directory)

   ## make html docs
   os.system('make html')
