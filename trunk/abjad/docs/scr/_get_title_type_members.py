from _get_module_members import _get_module_members
import os


def _get_title_type_members(source_full_path):

   #print source_full_path
   # starts as '/Users/foo/bar/abjad/trunk/abjad/tools/sequencetools/do_stuff.py'

   parts = [ ]
   for part in reversed(source_full_path.split(os.sep)):
      if not part == 'abjad':
         parts.insert(0, part)
      else:
         parts.insert(0, part)
         break

   # ends as 'abjad.tools.sequencetools.do_stuff'
   parts = '.'.join(parts)
   parts = parts[:-3]
   #print parts

   # name is something like 'apply_octavation' or 'Accidental'
   name = parts.split('.')[-1]
   #print name

   # module is in one of the tools packages
   if parts.startswith('abjad.tools.'):
      page_title = parts[12:]
      #print 'PAGE TITLE is %s' % page_title
      # if source file in tools package implements public helper function
      if name[0].islower():
         auto_type = 'autofunction'
         functions = _get_module_members(source_full_path, 'def')
      # if source file in tools package implements public class
      else:
         page_title = page_title.split('.')
         page_title = page_title[:-1]
         page_title = '.'.join(page_title)
         # page title is now something like pitchtools.NamedChromaticPitchClass
         auto_type = 'autoclass'
         functions = _get_module_members(source_full_path, 'class')
      public_functions = [x for x in functions if not x.startswith('_')]
      members = public_functions
      # check if file defines only private _get_measure_from_component(), for example
      if not members:
         #print 'NOT rendering %s ...' % page_title
         page_title = None

   # or is the exceptions module
   elif 'exceptions' in source_full_path:
      page_title = 'exceptions'
      auto_type = 'autoexception'
      members = _get_module_members(source_full_path, 'class')

   # or is a class file
   elif _get_module_members(source_full_path, 'class'):
      members = _get_module_members(source_full_path, 'class')
      if 1 < len(members):
         raise ValueError('%s defines more than 1 public class!' %
            source_full_path)
      page_title = members[0]
      auto_type = 'autoclass'

   # or contains public functions, like dfs(), outside of tools packages
   elif _get_module_members(source_full_path, 'def'):
      raise ValueError('no public helpers outside of tools packages!')

   # or else contains only non-documenting helper functions
   else:
      raise ValueError('unkonwn type of module content: %s.' % source_full_path)

   return page_title, auto_type, members
