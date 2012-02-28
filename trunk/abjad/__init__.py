from abjad.tools.importtools._import_functions_in_package_to_namespace import _import_functions_in_package_to_namespace
from abjad.tools import *
from abjad.tools.chordtools import Chord
from abjad.tools.containertools import Container
from abjad.tools.durationtools import Duration
from abjad.tools.iotools import f
from abjad.tools.iotools import p
from abjad.tools.iotools import play
from abjad.tools.iotools import show
from abjad.tools.measuretools import Measure
from abjad.tools.notetools import Note
from abjad.tools.resttools import Rest
from abjad.tools.scoretools import Score
from abjad.tools.stafftools import Staff
from abjad.tools.tuplettools import Tuplet
from abjad.tools.voicetools import Voice
from fractions import Fraction
import os
import sys

# import Abjad exceptions in Python __builtins__ namespace
_exceptions_path = os.path.join(__path__[0], 'exceptions')
_import_functions_in_package_to_namespace(_exceptions_path, __builtins__)

# check for prompt preference
from abjad.cfg._read_config_file import _read_config_file
if _read_config_file( )['use_abjad_prompt']:
    sys.ps1 = 'abjad> '
del _read_config_file

del cfg
del configurationtools
del core
del durationtools
del exceptions
del importtools
del interfaces
del mathtools
del timesignaturetools
del os
del pitcharraytools
del sequencetools
del sievetools
del sys
del threadtools
del tonalitytools
del tools

__version__ = '2.7'
