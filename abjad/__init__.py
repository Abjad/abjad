# -*- coding: utf-8 -*-


# warn on an outdated Python installation
import distutils.version
import platform
if not (
    distutils.version.LooseVersion('2.7.2') <
    distutils.version.LooseVersion(platform.python_version())
    ):
    print('WARNING: Abjad does not support Python versions less than 2.7.3.')
    print('WARNING: Upgrade your Python to 2.7.3 or higher.')
del platform
del distutils

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
from abjad.tools.durationtools import Duration
from abjad.tools.durationtools import Multiplier
from abjad.tools.durationtools import Offset
from abjad.tools.mathtools import Ratio
from abjad.tools.indicatortools import Accelerando
from abjad.tools.indicatortools import Articulation
from abjad.tools.indicatortools import Clef
from abjad.tools.indicatortools import Dynamic
from abjad.tools.indicatortools import Fermata
from abjad.tools.indicatortools import KeySignature
from abjad.tools.indicatortools import LilyPondCommand
from abjad.tools.indicatortools import Ritardando
from abjad.tools.indicatortools import Tempo
from abjad.tools.indicatortools import TimeSignature
from abjad.tools.markuptools import Markup
from abjad.tools.pitchtools import NamedPitch
from abjad.tools.scoretools import Chord
from abjad.tools.scoretools import Container
from abjad.tools.scoretools import Context
from abjad.tools.scoretools import Measure
from abjad.tools.scoretools import MultimeasureRest
from abjad.tools.scoretools import Note
from abjad.tools.scoretools import Rest
from abjad.tools.scoretools import Score
from abjad.tools.scoretools import Skip
from abjad.tools.scoretools import Staff
from abjad.tools.scoretools import StaffGroup
from abjad.tools.scoretools import Tuplet
from abjad.tools.scoretools import Voice
from abjad.tools.sequencetools import Sequence
from abjad.tools.spannertools import Beam
from abjad.tools.spannertools import Crescendo
from abjad.tools.spannertools import Decrescendo
from abjad.tools.spannertools import Glissando
from abjad.tools.spannertools import Hairpin
from abjad.tools.spannertools import Slur
from abjad.tools.spannertools import Tie
from abjad.tools.timespantools import Timespan
from fractions import Fraction

# import some frequently used functions for direct user access
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import graph
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import label
from abjad.tools.topleveltools import mutate
from abjad.tools.topleveltools import new
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import parse
from abjad.tools.topleveltools import play
from abjad.tools.topleveltools import persist
from abjad.tools.topleveltools import select
from abjad.tools.topleveltools import sequence
from abjad.tools.topleveltools import set_
from abjad.tools.topleveltools import show

# import custom exceptions into the builtins module
import os
from abjad.tools.systemtools.ImportManager import ImportManager
ImportManager.import_public_names_from_path_into_namespace(
    os.path.join(__path__[0], 'tools', 'exceptiontools'),
    __builtins__,
    )
del ImportManager
del os
del tools

# import version information
from abjad._version import __version_info__, __version__
del _version

def f(expr):
    print(format(expr, 'lilypond'))

from abjad import demos
from abjad import ext
from abjad import ly