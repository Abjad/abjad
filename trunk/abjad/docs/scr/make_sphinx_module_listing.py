from _append_class_options import _append_class_options
from _get_title_type_members import _get_title_type_members
from abjad.cfg.cfg import ABJADPATH
import os


def make_sphinx_module_listing(package_path, file):
   '''This function creates the files like chord.rst.

   Output looks like this:

   Chord
   ==========

   .. automodule:: abjad.components.Chord.chord

   .. autoclass:: abjad.components.Chord
      :members:
      :undoc-members:
      :show-inheritance:
      :inherited-members:

   Returns result as a string.
   '''
   
   #abjad_path = ABJADPATH.rstrip('/abjad')
   abjad_path = os.path.split(ABJADPATH)[0]
   source_full_path = os.path.join(abjad_path, package_path, file)
   file = file.split('.')[0]

   # TODO: tweak me to print accurate but minimal page and sidebar title #
   #package = os.path.join(package_path, file).replace(os.path.sep, '.')

   page_title, auto_type, members = _get_title_type_members(source_full_path)

#   print 'FOO!'
#   print page_title
#   print auto_type
#   print members
#   print 'BAR!'
#   print ''

   # if you want to generate NO api entry for a class of function,
   # then return page_title as None;
   # yes, this is hackish, but it works at least for now.
   if page_title is None:
      return None

   result = '%s\n' %  page_title
   result += '=' * (len(result) - 1)
   result += '\n\n'

   module = os.path.join(package_path, file)
   module = module.replace(os.path.sep, '.')
   #result += '.. automodule:: %s\n' % module
   #result += '\n'

   for member in members:

      # document public helper in tools package like sequencetools.zip_sequences_cyclically
      if auto_type == 'autofunction' and 'tools' in module:
         result += '.. %s:: abjad.tools.%s\n' % (auto_type, page_title)

      # document public class in tools package like pitchtools.NamedChromaticPitchClass
      elif auto_type == 'autoclass' and 'tools' in module:
         result += '.. %s:: abjad.tools.%s\n' % (auto_type, page_title)   
         result = _append_class_options(result)

      # document global public classes like Chord
      elif auto_type == 'autoclass' and not page_title.startswith('_') \
         and not page_title.endswith('Interface'):
         result += '.. %s:: abjad.%s\n' % (auto_type, page_title)   
         result = _append_class_options(result)

      # document public interface like ChordInterface
      elif auto_type == 'autoclass' and not page_title.startswith('_') \
         and (page_title.endswith('Interface') and 'Parentage' not in page_title):
         result += '.. %s:: %s.%s\n' % (auto_type, module, page_title)   
         result = _append_class_options(result)

      # do not document private classes like _ChordFormatter
      elif auto_type == 'autoclass' and page_title.startswith('_'):
         return None

      # do not document parentage interface:
      elif page_title == 'ParentageInterface':
         return None

      # shouldn't be anything else
      else:
         raise ValueError('unknown auto type "%s" or page title "%s".' % (auto_type, page_title))

   return result
