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
from abjad.tools.configurationtools import AbjadConfiguration
abjad_configuration = AbjadConfiguration()
del AbjadConfiguration

# import all tools packages
from abjad.tools import *

# import some frequently used classes for direct user access
from abjad.tools.chordtools import Chord
from abjad.tools.containertools import Container
from abjad.tools.durationtools import Duration
from abjad.tools.durationtools import Multiplier
from abjad.tools.durationtools import Offset
from abjad.tools.measuretools import Measure
from abjad.tools.notetools import Note
from abjad.tools.pitchtools import NamedPitch
from abjad.tools.resttools import Rest
from abjad.tools.scoretools import Score
from abjad.tools.stafftools import Staff
from abjad.tools.tuplettools import Tuplet
from abjad.tools.voicetools import Voice
from fractions import Fraction

# import some frequently used functions for direct user access
from abjad.tools.iotools import f
from abjad.tools.iotools import p
from abjad.tools.iotools import play
from abjad.tools.iotools import show
from abjad.tools.iotools import z
from abjad.tools.mutationtools import mutate
from abjad.tools.mutationtools.AttributeInspectionAgent import inspect
from abjad.tools.selectiontools import select

# import custom exceptions into the builtins module
import os
from abjad.tools.importtools.ImportManager import ImportManager
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
