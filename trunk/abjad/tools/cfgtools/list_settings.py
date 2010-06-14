from abjad.cfg import cfg
import pprint
import types


def list_settings( ):
   '''List Abjad config settings::

      abjad> cfgtools.list_settings( )
      ('ABJADCONFIG', '/Users/foo/bar/.abjad/config.py')
      ('ABJADPATH', '/Users/foo/bar/Documents/abjad/trunk/abjad/')
      ('ABJADVERSIONFILE', '/Users/foo/bar/Documents/abjad/trunk/abjad/.version')
      ('HOME', '/Users/foo/bar')

   Abjad config settings are defined in ``abjad/cfg/cfg.py``.
   '''

   for key, value in sorted(vars(cfg).items( )):
      if not isinstance(value, types.ModuleType):
         if not key.startswith('_'):
            pprint.pprint((key, value))
