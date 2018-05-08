import os
if 'topleveltools' in os.path.abspath('.'):
    message = 'do not start Abjad from topleveltools directory (inspect.py).'
    raise Exception(message)
del os

from fractions import Fraction
try:
    from quicktions import Fraction  # type: ignore
except ImportError:
    pass

# ensure that the ~/.abjad directory and friends are setup
# and instantiate Abjad's configuration singleton
from abjad.tools.systemtools.AbjadConfiguration import AbjadConfiguration
abjad_configuration = AbjadConfiguration()
del AbjadConfiguration

# import all tools packages
from abjad.tools import *
from abjad.tools.abctools import *
from abjad.tools.datastructuretools import *

index = Pattern.index
index_all = Pattern.index_all
index_first = Pattern.index_first
index_last = Pattern.index_last

from abjad.tools.exceptiontools import *
from abjad.tools.indicatortools import *
from abjad.tools.instrumenttools import *
from abjad.tools.lilypondfiletools import *
from abjad.tools.lilypondnametools import *
from abjad.tools.markuptools import *
from abjad.tools.metertools import *
from abjad.tools.pitchtools import *
from abjad.tools.schemetools import *
from abjad.tools.scoretools import *
from abjad.tools.segmenttools import *
from abjad.tools.spannertools import *
from abjad.tools.systemtools import *
from abjad.tools.topleveltools import *

# import all the way down to module to satisfy mypy:
from abjad.tools.mathtools.Enumerator import Enumerator
from abjad.tools.mathtools.NonreducedFraction import NonreducedFraction
from abjad.tools.mathtools.NonreducedRatio import NonreducedRatio
from abjad.tools.mathtools.Ratio import Ratio

# timespantools classes (but not functions)
from abjad.tools.timespantools.AnnotatedTimespan import AnnotatedTimespan
from abjad.tools.timespantools.Timespan import Timespan
from abjad.tools.timespantools.TimespanInequality import TimespanInequality
from abjad.tools.timespantools.TimespanList import TimespanList

# rhythm-maker static methods
from abjad.tools.rhythmmakertools.SilenceMask import SilenceMask
from abjad.tools.rhythmmakertools.SustainMask import SustainMask
silence = SilenceMask.silence
sustain = SustainMask.sustain

# import version information
from abjad._version import __version_info__, __version__
del _version

from abjad import book
from abjad import cli
from abjad import demos
from abjad import ly

# HOUSECLEANING HELPER: uncomment below and run tests;
#                       checks for hasattr() calls against properties:
#def hasattr_warn(argument, name, original_hasattr=hasattr):
#    if original_hasattr(argument.__class__, name):
#        value = getattr(argument.__class__, name)
#        if isinstance(value, property):
#            message = 'WARNING: {}.{} is a property!'
#            message = message.format(argument.__class__.__name__, name)
#            raise Exception(message)
#    return original_hasattr(argument, name)
#__builtins__['hasattr'] = hasattr_warn
