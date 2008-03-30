from os import listdir

_fns = listdir(__path__[0])
_modules = [_fn[ : -3] for _fn in _fns 
   if _fn.endswith('.py') and not _fn.startswith('_')]

for _module in sorted(_modules):
   exec('from %s import *' % _module)

def check_cleaner(locals):
   from types import TypeType
   for _key, _value in locals.items( ):
      if not isinstance(_value, TypeType) and _key != 'check_cleaner':
         del(locals[_key])
check_cleaner(locals( ))
del check_cleaner
