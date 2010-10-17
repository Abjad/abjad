from abjad.cfg.cfg import ABJADPATH
import os


def list_templates( ):
   '''List templates::

      abjad> cfgtools.list_templates( )
      ['coventry.ly', 'lagos.ly', 'oedo.ly', 'paris.ly', 'tangiers.ly', 'thebes.ly', 'tirnaveni.ly']

   Return list of zero or more strings.
   '''

   file_names = [ ]
   for file_name in os.listdir(os.path.join(ABJADPATH, 'templates')):
      if file_name.endswith('.ly'):
         if not file_name.startswith('_'):
            file_names.append(file_name)
   return file_names
