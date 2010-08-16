from abjad.cfg.cfg import ABJADPATH
from _list_toplevel_docmenting_abjad_directories import _list_toplevel_documeting_abjad_diretories
from _filter_directories import _filter_directories
import os


def _get_documenting_abjad_modules( ):
   '''Return a list of documenting Abjad modules.
   '''

   modules = [ ]
   toplevel_documenting_directories = _list_toplevel_documenting_abjad_directories( )
   for current_root, dirs, files in os.walk(ABJADPATH):
      if '.svn' not in current_root:
         if 'test' not in current_root:
            for file in files:
               if file.endswith('.py'):
                  if not file.startswith('__'):
                     module = os.path.join(current_root, file)
                     modules.append(module)
   return modules
   

if __name__ == '__main__':
   modules = _get_all_abjad_names( )
   for x in modules:
      print x
