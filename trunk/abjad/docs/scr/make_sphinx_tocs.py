from _write_file_interactive import _write_file_interactive
from abjad.cfg.cfg import ABJADPATH
from build_doc_tree import build_doc_tree
from make_sphinx_toc import make_sphinx_toc
import os


def make_sphinx_tocs(interactive = None):
   '''Walk entire Abjad codebase and make Sphinx TOCs automatically.
   '''

   # determine interactivity
   os.system('clear')
   api_doc_path = os.path.join(ABJADPATH, 'docs', 'chapters', 'api')
   modules_visited = [ ]
   if interactive is None:
      interactive = raw_input('Run script in interactive mode? [Y/n]: ')
   elif interactive == True:
      interactive = 'y'
   elif interactive == False:
      interactive = 'n'
   else:
      raise ValueError('unkonwn value for interactive: %s' % interactive)

   # make sphinx tocs
   os.system('clear')
   build_doc_tree(ABJADPATH, api_doc_path, interactive)
   toc = make_sphinx_toc()
   index = os.path.join(api_doc_path, 'index.rst')
   _write_file_interactive(toc, index, interactive)

   # print stop
   print ''
   print '... Done.'
   print ''
