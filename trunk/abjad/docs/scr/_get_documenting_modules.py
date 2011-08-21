from _get_documenting_directories import _get_documenting_directories
from abjad.cfg.cfg import ABJADPATH
import os


def _get_documenting_modules():
   '''Return a list of Abjad modules to search for
   classes and functions to document in the public API.
   '''

   modules = [ ]
   documenting_directories = _get_documenting_directories()
   for documenting_directory in documenting_directories:
      documenting_directory = os.path.join(ABJADPATH, documenting_directory)
      for current_root, dirs, files in os.walk(documenting_directory):
         if '.svn' not in current_root:
            if 'test' not in current_root:
               for file in files:
                  if file.endswith('.py'):
                     if not file.startswith('__'):
                        module = os.path.join(current_root, file)
                        modules.append(module)
   return modules
   

if __name__ == '__main__':
   modules = _get_documenting_modules()
   for x in modules:
      print x
