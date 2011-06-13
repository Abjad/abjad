from abjad.tools.importtools._import_functions_in_package_to_namespace import _import_functions_in_package_to_namespace
import os

## import exceptions
_exceptions_path = os.path.join(__path__[0], 'exceptions')
_import_functions_in_package_to_namespace(_exceptions_path, __builtins__)

from fractions import Fraction
from abjad.tools.durtools import Duration
from components import *
from abjad.tools import *
del cfgtools
del layouttools
del pitcharraytools
del sievetools
del tonalitytools
import macros

## import tools and io
from abjad.tools.iotools import f
from abjad.tools.iotools import play
from abjad.tools.iotools import show

import sys
sys.ps1 = 'abjad> '
del sys
del os

del cfg
del components
del core
del importtools
del exceptions
del interfaces
del tools
