from abjad.tools.importtools._import_functions_in_package_to_namespace import \
   _import_functions_in_package_to_namespace

## Do not use dynamic import code any more;
## hand manage global package contents instead.
'''
## create list of directories to skip
_skip = [
   'book', 'checks', 'demos', 'docs', 'exceptions', 
   'scr', '.svn', 'test', 'tools',
   ]

## import all public classes, including interfaces
_import_functions_in_package_to_namespace(__path__[0], globals( ), _skip)

## remove AccidentalInterface, BeamInterface and other interfaces.
for _key in globals( ).keys( ):
   if _key.endswith('Interface') or _key.endswith('Aggregator'):
      del(globals( )[_key])
'''

## reimport import tools since they were removed after previous import
from abjad.tools.importtools._import_functions_in_package_to_namespace import \
   _import_functions_in_package_to_namespace
import os

## import exceptions
_exceptions_path = os.path.join(__path__[0], 'exceptions')
#_import_functions_in_package_to_namespace(_exceptions_path, __builtins__, _skip)
_import_functions_in_package_to_namespace(_exceptions_path, __builtins__)

from fractions import Fraction
Rational = Fraction
del Fraction

from components import *
from marks import *
from abjad.tools import *
import macros

## import tools and io
from abjad.tools.iotools import f
from abjad.tools.iotools import play
from abjad.tools.iotools import show

import sys
sys.ps1 = 'abjad> '
del sys
del os
del importtools
