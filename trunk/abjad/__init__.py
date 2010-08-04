from abjad.tools.importtools._import_functions_in_package_to_namespace import \
   _import_functions_in_package_to_namespace

#print '1'
## create list of directories to skip
_skip = [
   'book', 'checks', 'demos', 'documentation', 'exceptions', 
   'scr', '.svn', 'test', 'tools',
   ]

#print '2'
## import all public classes, including interfaces
_import_functions_in_package_to_namespace(__path__[0], globals( ), _skip)

#print '3'
## remove AccidentalInterface, BeamInterface and other interfaces.
for _key in globals( ).keys( ):
   if _key.endswith('Interface') or _key.endswith('Aggregator'):
      del(globals( )[_key])

#print '4'
## reimport import tools since they were removed after previous import
from abjad.tools.importtools._import_functions_in_package_to_namespace import \
   _import_functions_in_package_to_namespace
import os

## import exceptions
_exceptions_path = os.path.join(__path__[0], 'exceptions')
_import_functions_in_package_to_namespace(_exceptions_path, __builtins__, _skip)

## import tools and io
from abjad.tools.iotools import f
from abjad.tools.iotools import play
from abjad.tools.iotools import show
from abjad.tools import *

import sys
sys.ps1 = 'abjad> '
del sys
del os
del importtools
