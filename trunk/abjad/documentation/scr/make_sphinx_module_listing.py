from abjad.cfg.cfg import ABJADPATH
from _get_module_members import _get_module_members
import os

def make_sphinx_module_listing(package_path, file):
   source_full_path = os.path.join(ABJADPATH.rstrip('/abjad'), 
      package_path, file)
   file = file.split('.')[0]
   ## TODO: tweak me to print accurate but minimal page and sidebar title ##
   #package = os.path.join(package_path, file).replace(os.path.sep, '.')
   package = file
   result = '%s\n' %  package
   result += '=' * (len(result) - 1)
   result += '\n\n'

   module = os.path.join(package_path, file)
   module = module.replace(os.path.sep, '.')
   result += '.. automodule:: %s\n' % module
   result += '\n'

   members = _get_module_members(source_full_path, 'class')
   for member in members:

      ## TODO: tweak me to get accurate but minimal search path ##
      if member.startswith('_'):
         result += '.. autoclass:: %s.%s\n' % (module, member)
      else:
         result += '.. autoclass:: abjad.%s\n' % member

      result += '   :members:\n'
      result += '   :undoc-members:\n'
      result += '   :show-inheritance:\n'
      result += '   :inherited-members:\n'
      result += '\n'

   members = _get_module_members(source_full_path, 'def')
   for member in members:
      result += '.. autofunction:: %s.%s\n' % (module, member)
   return result

