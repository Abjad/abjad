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

try:
    from quicktions import Fraction
except ImportError:
    from fractions import Fraction

# ensure that the ~/.abjad directory and friends are setup
# and instantiate Abjad's configuration singleton
from abjad.tools.systemtools.AbjadConfiguration import AbjadConfiguration
abjad_configuration = AbjadConfiguration()
del AbjadConfiguration

# import all tools packages
from abjad.tools import *
from abjad.tools.abctools import *
from abjad.tools.datastructuretools import *
from abjad.tools.durationtools import *
from abjad.tools.exceptiontools import *
from abjad.tools.expressiontools import *
from abjad.tools.indicatortools import *
from abjad.tools.lilypondfiletools import *
from abjad.tools.markuptools import *
from abjad.tools.patterntools import *
from abjad.tools.pitchtools import *
from abjad.tools.schemetools import *
from abjad.tools.selectiontools import *
from abjad.tools.selectortools import *
from abjad.tools.sequencetools import *
from abjad.tools.spannertools import *
from abjad.tools.spannertools import *
from abjad.tools.topleveltools import *

# mathtools classes (but not functions)
from abjad.tools.mathtools import Infinity
Infinity = Infinity()
from abjad.tools.mathtools import NonreducedFraction
from abjad.tools.mathtools import NonreducedRatio
from abjad.tools.mathtools import Ratio
from abjad.tools.metertools import Meter
from abjad.tools.metertools import MeterList

# scoretools classes (but not functions)
from abjad.tools.scoretools import Chord
from abjad.tools.scoretools import Cluster
from abjad.tools.scoretools import Component
from abjad.tools.scoretools import Container
from abjad.tools.scoretools import Context
from abjad.tools.scoretools import FixedDurationTuplet
from abjad.tools.scoretools import GraceContainer
from abjad.tools.scoretools import Leaf
from abjad.tools.scoretools import Measure
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

from abjad.tools.timespantools import Timespan

# rhythm-maker functions (but not classes)
from abjad.tools.rhythmmakertools import silence
from abjad.tools.rhythmmakertools import silence_all
from abjad.tools.rhythmmakertools import silence_every
from abjad.tools.rhythmmakertools import silence_except
from abjad.tools.rhythmmakertools import silence_first
from abjad.tools.rhythmmakertools import silence_last
from abjad.tools.rhythmmakertools import sustain
from abjad.tools.rhythmmakertools import sustain_all
from abjad.tools.rhythmmakertools import sustain_every
from abjad.tools.rhythmmakertools import sustain_first
from abjad.tools.rhythmmakertools import sustain_last

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

def f(argument):
    if hasattr(argument, '_publish_storage_format'):
        print(format(argument, 'storage'))
    else:
        print(format(argument, 'lilypond'))

from abjad import demos
from abjad import ext
from abjad import ly
