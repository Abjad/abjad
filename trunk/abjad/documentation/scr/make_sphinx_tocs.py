from _write_file_interactive import _write_file_interactive
from abjad.cfg.cfg import ABJADPATH
from build_doc_tree import build_doc_tree
from make_sphinx_toc import make_sphinx_toc
import os


def make_sphinx_tocs( ):
   '''Walk entire Abjad codebase and make Sphinx TOCs automatically.'''

   os.system('clear')
   api_doc_path = os.path.join(ABJADPATH, 'documentation', 'chapters', 'api')
   modules_visited = [ ]
   interactive = raw_input('Run script in interactive mode? [Y/n]: ')
   os.system('clear')
   print 'Making Sphinx TOCs ... '
   build_doc_tree(ABJADPATH, api_doc_path, interactive)
   toc = make_sphinx_toc( )
   index = os.path.join(api_doc_path, 'index.rst')
   _write_file_interactive(toc, index, interactive)
