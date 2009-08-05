from _get_all_abjad_names import _get_all_abjad_names
import os


def _get_public_abjad_names( ):
   '''Return list of name dictionaries for only those names
   that appear in directories which are not forbideen.
   '''

   public_names = [ ]
   forbidden_directories = ['.svn', 'book', 'cfg', 'checks', 'demos',
      'documentation', 'scm', 'scr', 'test', ]

   for name in _get_all_abjad_names( ):
      
      for forbidden_directory in forbidden_directories:
         module_path_parts = name['module'].split(os.sep)
         if forbidden_directory in module_path_parts:
            break
      else:
         public_names.append(name)

   return public_names
