from abjad.tools.importtools._import_functions_in_package_to_namespace import _import_functions_in_package_to_namespace
from abjad.components import *
from abjad.tools import *
from abjad.tools.durtools import Duration
from abjad.tools.iotools import f
from abjad.tools.iotools import play
from abjad.tools.iotools import show
from fractions import Fraction
import macros
import os
import sys

## import Abjad exceptions in Python __builtins__ namespace
_exceptions_path = os.path.join(__path__[0], 'exceptions')
_import_functions_in_package_to_namespace(_exceptions_path, __builtins__)

sys.ps1 = 'abjad> '

del cfg
del cfgtools
del components
del core
del exceptions
del formattools
del importtools
del interfaces
del layouttools
del os
del pitcharraytools
del sievetools
del sys
del tempotools
del threadtools
del tonalitytools
del tools
del verticalitytools
