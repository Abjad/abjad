from os import listdir

_checks = listdir(__path__[0])
_checks = [_check[ : -3] for _check in _checks if 
            _check.startswith('check_') and _check.endswith('.py')]

for _check in sorted(_checks):
   exec('from %s import *' % _check)

def check_cleaner(locals):
   from types import FunctionType
   for _key, _value in locals.items( ):
      if not (isinstance(_value, FunctionType) and _key.startswith('check_')):
         del(locals[_key])
check_cleaner(locals( ))
del check_cleaner
