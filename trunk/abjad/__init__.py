import platform

_python_version = platform.python_version()
if not _python_version.startswith('2.7'):
    print 'WARNING: Abjad no longer supports versions of Python less than 2.7!'
    print 'WARNING: Please upgrade your version of Python to 2.7!'

import readline
import rlcompleter
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")

# setup .abjad directory and friends (if not already handled elsewhere)
# configurationtools.setup_abjad_directory_silently()
from abjad.tools.configurationtools import AbjadConfig
ABJCFG = AbjadConfig()
del AbjadConfig

from abjad.tools.importtools._import_functions_in_package_to_namespace import \
    _import_functions_in_package_to_namespace
from abjad.tools import *
from abjad.tools.chordtools import Chord
from abjad.tools.containertools import Container
from abjad.tools.durationtools import Duration
from abjad.tools.durationtools import Multiplier
from abjad.tools.durationtools import Offset
from abjad.tools.iotools import f
from abjad.tools.iotools import p
from abjad.tools.iotools import play
from abjad.tools.iotools import show
from abjad.tools.iotools import z
from abjad.tools.measuretools import Measure
from abjad.tools.notetools import Note
from abjad.tools.resttools import Rest
from abjad.tools.scoretools import Score
from abjad.tools.stafftools import Staff
from abjad.tools.tuplettools import Tuplet
from abjad.tools.voicetools import Voice
from fractions import Fraction
import os

# import Abjad exceptions in __builtins__ namespace
_exceptions_path = os.path.join(__path__[0], 'tools', 'exceptiontools')
_import_functions_in_package_to_namespace(_exceptions_path, __builtins__)

del os
del platform
del readline
del rlcompleter
del tools

__version__ = '2.12'
