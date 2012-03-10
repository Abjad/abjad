import os


_fns = os.listdir(__path__[0])
_modules = [_fn[:-3] for _fn in _fns if _fn.endswith('.py') and not _fn.startswith('_')]
_modules.remove('Check')

for _module in sorted(_modules):
   exec('from %s import *' % _module)

def check_cleaner(locals):
   import types
   from abjad.checks.Check import Check
   for _key, _value in locals.items():
      if _key == 'check_cleaner' or \
         (isinstance(_value, types.TypeType) and \
         'checks' in _value.__module__):
         pass
      else:
         del(locals[_key])
check_cleaner(locals())
del check_cleaner
del Check
