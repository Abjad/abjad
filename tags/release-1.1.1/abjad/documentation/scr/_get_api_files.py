from _filter_directories import  _filter_directories
from _filter_files import _filter_files
from abjad.cfg.cfg import ABJADPATH
import os


def _get_api_files( ):
   for current_root, dirs, files in os.walk(ABJADPATH):
      ## removed unwanted dirs and files.
      filtered_dirs = ['.svn', 'cfg', 'checks', 'demos', 'documentation',
         'scm', 'scr', 'test', ]
      _filter_directories(dirs, filtered_dirs)
      _filter_files(files)
      dirs.sort( )
      files.sort( )
      print current_root, dirs, files

