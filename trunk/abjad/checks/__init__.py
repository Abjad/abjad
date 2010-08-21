import os


_fns = os.listdir(__path__[0])
_modules = [_fn[:-3] for _fn in _fns 
   if _fn.endswith('.py') and not _fn.startswith('_')]

for _module in sorted(_modules):
   exec('from %s import *' % _module)

def check_cleaner(locals):
   #from types import TypeType
   import types
   from abjad.checks._Check import _Check
   for _key, _value in locals.items( ):
      #if not isinstance(_value, types.TypeType) and _key != 'check_cleaner':
      #   del(locals[_key])
      if _key == 'check_cleaner' or \
         (isinstance(_value, types.TypeType) and \
         'checks' in _value.__module__):
         pass
      else:
         del(locals[_key])
check_cleaner(locals( ))
del check_cleaner
