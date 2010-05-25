from _get_module_members import _get_module_members
from abjad.cfg.cfg import ABJADPATH
import os


def make_sphinx_module_listing(package_path, file):
   '''This function creates the files like accidental.rst.
   Output looks like this:

   Accidental
   ==========

   .. automodule:: abjad.accidental.accidental

   .. autoclass:: abjad.Accidental
      :members:
      :undoc-members:
      :show-inheritance:
      :inherited-members:
   '''
   
   source_full_path = os.path.join(
      ABJADPATH.rstrip('/abjad'), package_path, file)
   file = file.split('.')[0]

   ## TODO: tweak me to print accurate but minimal page and sidebar title ##
   #package = os.path.join(package_path, file).replace(os.path.sep, '.')

   page_title, auto_type, members = _get_title_type_members(source_full_path)

#   print 'FOO!'
#   print page_title
#   print auto_type
#   print members
#   print 'BAR!'
#   print ''
#   #if members and 'Crescendo' in members:
#   #if 'hairpin' in page_title:
#   #   raise Exception
#   raise Exception

   ## if you want to generate NO api entry for a class of function,
   ## then return page_title as None;
   ## yes, this is hackish, but it works at least for now.
   if page_title is None:
      return None

   result = '%s\n' %  page_title
   result += '=' * (len(result) - 1)
   result += '\n\n'

   module = os.path.join(package_path, file)
   module = module.replace(os.path.sep, '.')
   result += '.. automodule:: %s\n' % module
   result += '\n'

   for member in members:

      ## tool like .. autofunction:: listtools.abjad.tools.repeat_to_length
      if auto_type == 'autofunction' and 'tools' in module:
         result += '.. %s:: abjad.tools.%s\n' % (auto_type, page_title)

      ## class like .. autoclass:: abjad.Accidental
      elif auto_type == 'autoclass' and not page_title.startswith('_') \
         and not page_title.endswith('Interface') \
         and not page_title.endswith('Aggregator'):
         result += '.. %s:: abjad.%s\n' % (auto_type, page_title)   
         result = _append_class_options(result)

      ## interface .. autoclass:: abjad.accidental.interface.AccidentalInterface
      elif auto_type == 'autoclass' and not page_title.startswith('_') \
         and (page_title.endswith('Interface') or 
         page_title.endswith('Aggregator')):
         result += '.. %s:: %s.%s\n' % (auto_type, module, page_title)   
         result = _append_class_options(result)

      ## private _AccidentalInterface is now public AccidentalInterface
      elif auto_type == 'autoclass' and page_title.startswith('_'):
         return None

      ## shouldn't be anything else
      else:
         raise ValueError('unknown autodoc type!')

   return result


def _get_title_type_members(source_full_path):

   ## starts as '/Users/foo/bar/abjad/trunk/abjad/tools/listtools/do_stuff.py'
   parts = [ ]
   for part in reversed(source_full_path.split(os.sep)):
      if not part == 'abjad':
         parts.insert(0, part)
      else:
         parts.insert(0, part)
         break
   ## ends as 'abjad.tools.listtools.do_stuff'
   parts = '.'.join(parts)
   parts = parts[:-3]
   #print parts

   ## module is either in one of the tools packages
   if parts.startswith('abjad.tools.'):
      page_title = parts[12:]
      #print 'PAGE TITLE is %s' % page_title
      auto_type = 'autofunction'
      functions = _get_module_members(source_full_path, 'def')
      public_functions = [x for x in functions if not x.startswith('_')]
      members = public_functions
      ## check if file defines only private _measure_get( ), for example
      if not members:
         #print 'NOT rendering %s ...' % page_title
         page_title = None

   ## or is the exceptions module
   elif 'exceptions' in source_full_path:
      page_title = 'exceptions'
      auto_type = 'autoexception'
      members = _get_module_members(source_full_path, 'class')

   ## or is a class file
   elif _get_module_members(source_full_path, 'class'):
      members = _get_module_members(source_full_path, 'class')
      if 1 < len(members):
         raise ValueError('%s defines more than 1 public class!' %
            source_full_path)
      page_title = members[0]
      auto_type = 'autoclass'

   ## or contains public functions, like dfs( ), outside of tools packages
   elif _get_module_members(source_full_path, 'def'):
      members = _get_module_members(source_full_path, 'def')
      members = [x for x in members if not x.startswith('_')]
      if 1 < len(members):
         raise ValueError('%s defines more than 1 public function!' %
            source_full_path)
      page_title = members[0] # FIXME!
      auto_type = 'autofunction'

   ## or else contains only non-documenting helper functions
   else:
      raise ValueError('Unkonwn type of module content.')
      #print 'NOTE: nothing to document in %s' % source_full_path
      #page_title, auto_type, members = None, None, None

   return page_title, auto_type, members


def _append_class_options(result):
   result += '   :members:\n'
   result += '   :undoc-members:\n'
   result += '   :show-inheritance:\n'
   result += '   :inherited-members:\n'
   return result
