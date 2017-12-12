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


import os
if 'topleveltools' in os.path.abspath('.'):
    message = 'do not start Abjad from topleveltools directory (inspect.py).'
    raise Exception(message)
del os

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

# instantiate ordinal constants
Identity = OrdinalConstant('identity', 0, 'Identity')
Less = OrdinalConstant('value', -1, 'Less')
More = OrdinalConstant('value', 1, 'More')
Exact = OrdinalConstant('value', 0, 'Exact')
Left = OrdinalConstant('x', -1, 'Left')
Right = OrdinalConstant('x', 1, 'Right')
Both = OrdinalConstant('x', 0, 'Both')
Center = OrdinalConstant('y', 0, 'Center')
Up = OrdinalConstant('y', 1, 'Up')
Down = OrdinalConstant('y', -1, 'Down')
Top = OrdinalConstant('y', 1, 'Top')
Bottom = OrdinalConstant('y', -1, 'Bottom')

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
from abjad.tools.pitchtools import *
from abjad.tools.schemetools import *
from abjad.tools.scoretools import *
from abjad.tools.segmenttools import *
from abjad.tools.spannertools import *
from abjad.tools.systemtools import *
from abjad.tools.topleveltools import *

# mathtools classes (but not functions)
from abjad.tools.mathtools import Infinity
Infinity = Infinity()
from abjad.tools.mathtools import NegativeInfinity
NegativeInfinity = NegativeInfinity()

from abjad.tools.mathtools import Enumerator
from abjad.tools.mathtools import NonreducedFraction
from abjad.tools.mathtools import NonreducedRatio
from abjad.tools.mathtools import Ratio
from abjad.tools.metertools import Meter
from abjad.tools.metertools import MeterList
from abjad.tools.metertools import MeterManager
from abjad.tools.metertools import MetricAccentKernel
from abjad.tools.metertools import OffsetCounter

# timespantools classes (but not functions)
from abjad.tools.timespantools import AnnotatedTimespan
from abjad.tools.timespantools import Timespan
from abjad.tools.timespantools import TimespanInequality
from abjad.tools.timespantools import TimespanList

# rhythm-maker static methods
from abjad.tools.rhythmmakertools import SilenceMask
from abjad.tools.rhythmmakertools import SustainMask
silence = SilenceMask.silence
sustain = SustainMask.sustain

# import custom exceptions into the builtins module
import os
from abjad.tools.systemtools.ImportManager import ImportManager
ImportManager.import_public_names_from_path_into_namespace(
    os.path.join(__path__[0], 'tools', 'exceptiontools'),
    __builtins__,
    )
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
