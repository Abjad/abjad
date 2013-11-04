# -*- encoding: utf-8 -*-

# warn on an outdated Python installation
import platform
if not platform.python_version() in (('2.7.3', '2.7.4', '2.7.5')):
    print 'WARNING: Abjad no longer supports' + \
        ' versions of Python less than 2.7.3!'
    print 'WARNING: Please upgrade your' + \
        ' version of Python to 2.7.3, 2.7.4 or 2.7.5!'
del platform

# set up tab completion
try:
    import readline
    import rlcompleter
    if readline.__doc__ is not None and 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    del readline
    del rlcompleter
except ImportError:
    pass

# ensure that the ~/.abjad directory and friends are setup,
# and instantiate Abjad's configuration singleton
from abjad.tools.systemtools.AbjadConfiguration import AbjadConfiguration
abjad_configuration = AbjadConfiguration()
del AbjadConfiguration

# import all tools packages
from abjad.tools import *

# import some frequently used classes for direct user access
from abjad.tools.scoretools import Container
from abjad.tools.durationtools import Duration
from abjad.tools.durationtools import Multiplier
from abjad.tools.durationtools import Offset
from abjad.tools.pitchtools import NamedPitch
from abjad.tools.scoretools import Chord
from abjad.tools.scoretools import Measure
from abjad.tools.scoretools import Note
from abjad.tools.scoretools import Rest
from abjad.tools.scoretools import Score
from abjad.tools.scoretools import Staff
from abjad.tools.scoretools import Tuplet
from abjad.tools.scoretools import Voice
from fractions import Fraction

# import some frequently used functions for direct user access
from abjad.tools.functiontools import attach
from abjad.tools.functiontools import mutate
from abjad.tools.functiontools import override
from abjad.tools.functiontools import parse
from abjad.tools.functiontools import play
from abjad.tools.functiontools import select
from abjad.tools.functiontools import show
from abjad.tools.iotools import f
from abjad.tools.iotools import z
from abjad.tools.mutationtools.AttributeInspectionAgent import inspect

# import custom exceptions into the builtins module
import os
from abjad.tools.systemtools.ImportManager import ImportManager
ImportManager.import_public_names_from_filesystem_path_into_namespace(
    os.path.join(__path__[0], 'tools', 'exceptiontools'),
    __builtins__,
    )
del ImportManager
del os
del tools

# import version information
from abjad._version import __version_info__, __version__
del _version
