from _get_all_abjad_names import _get_all_abjad_names
import os


def _get_public_abjad_names( ):
   '''Return list of names of public Abjad classes and functions.
   Public classes and functions meet two criteria.
   First criterion is name that does not begin in underscore.
   Second criterion is that file is not housed in nondocumenting directory.
   Each list entry has the form of a dictionary with three items.
   The dictionary keys are 'name', 'kind', 'module'.
   '''

   public_names = [ ]
   ## TODO: nondocumeting directories should be identified as such
   ##       in the __init__.py of the directory.
   ##       The enumeration below can then be removed.
   forbidden_directories = ['.svn', 'book', 'cfg', 'checks', 'demos',
      'docs', 'scm', 'scr', 'test', ]

   for name in _get_all_abjad_names( ):
      for forbidden_directory in forbidden_directories:
         module_path_parts = name['module'].split(os.sep)
         if forbidden_directory in module_path_parts:
            break
         if name['name'].startswith('_'):
            break
      else:
         public_names.append(name)

   return public_names
