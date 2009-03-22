from abjad.tools.imports.get_topmost_module import _get_topmost_module
import os


def _get_functions_in_module(module_file):
   '''Collects and returns all functions defined in module_file.'''
   result = [ ]
   module_file.replace(os.sep, '.')
   mod = _get_topmost_module(module_file)
   for key, value in mod.__dict__.items( ):
      if getattr(value, '__module__', None) == module_file:
         #print '"%s" in module %s ' % (key, module_file)
         result.append(value)
   return result

