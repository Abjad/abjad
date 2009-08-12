import pprint
import types


def list_settings( ):
   '''Pretty-print Abjad config settings.

   ::

      abjad> cfgtools.list_settings( )
      ('ABJADCONFIG', '/Users/foo/bar/.abjad/config.py')
      ('ABJADPATH', '/Users/foo/bar/Documents/abjad/trunk/abjad/')
      ('ABJADVERSIONFILE', '/Users/foo/bar/Documents/abjad/trunk/abjad/.version')
      ('home_path', '/Users/foo/bar')

   Function lists public attribues of the ``abjad/cfg/cfg.py`` module.
   '''

   from abjad.cfg import cfg

   for key, value in sorted(vars(cfg).items( )):
      if not isinstance(value, types.ModuleType):
         if not key.startswith('_'):
            pprint.pprint((key, value))
