from os import listdir

_checks = listdir(__path__[0])
_checks = [_check[ : -3] for _check in _checks if 
            _check.startswith('check_') and _check.endswith('.py')]

for _check in sorted(_checks):
   exec('from %s import *' % _check)

del listdir, _checks, _check
