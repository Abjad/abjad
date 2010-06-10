from abjad.tools.imports.import_functions_in_package_to_namespace import \
   _import_functions_in_package_to_namespace

## create list of directories to skip
_skip = [
   'book', 'checks', 'demos', 'documentation', 'exceptions', 
   'scr', '.svn', 'test', 'tools',
   ]

## import all public classes, including interfaces
_import_functions_in_package_to_namespace(__path__[0], globals( ), _skip)

## remove AccidentalInterface, BeamInterface and other interfaces.
for _key in globals( ).keys( ):
   if _key.endswith('Interface') or _key.endswith('Aggregator'):
      del(globals( )[_key])

## reimport import tools since they were removed after previous import
from abjad.tools.imports.import_functions_in_package_to_namespace import \
   _import_functions_in_package_to_namespace
import os

## import exceptions
_exceptions_path = os.path.join(__path__[0], 'exceptions')
_import_functions_in_package_to_namespace(
   _exceptions_path, __builtins__, _skip)

## import tools and io
from abjad.tools.io import f
from abjad.tools.io import log
from abjad.tools.io import ly
from abjad.tools.io import pdf
from abjad.tools.io import play
from abjad.tools.io import redo
from abjad.tools.io import show
from abjad.tools import *

import sys
sys.ps1 = 'abjad> '
del sys
