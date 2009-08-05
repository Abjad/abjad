import pprint
import types


def list_settings( ):
   '''List settings defined in abjad/cfg/cfg.py module.'''

   from abjad.cfg import cfg

   for key, value in sorted(vars(cfg).items( )):
      if not isinstance(value, types.ModuleType):
         if not key.startswith('_'):
            pprint.pprint((key, value))
