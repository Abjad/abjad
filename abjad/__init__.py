from fractions import Fraction  # noqa

try:
    from quicktions import Fraction  # type: ignore
except ImportError:
    pass

from abjad.enums import *
from abjad.exceptions import *

# ensure that the ~/.abjad directory and friends are setup
# and instantiate Abjad's configuration singleton
from abjad.system.AbjadConfiguration import AbjadConfiguration

abjad_configuration = AbjadConfiguration()
del AbjadConfiguration

# import parser
from abjad import parser

# import all tools packages
from abjad.system import *
from abjad.utilities import *

# typings after utilities (for Expression)
from abjad.typings import *

index = Pattern.index
index_all = Pattern.index_all
index_first = Pattern.index_first
index_last = Pattern.index_last

from abjad.indicators import *
from abjad.instruments import *
from abjad.lilypondfile import *
from abjad.lilypondnames import *
from abjad.markups import *
from abjad.meter import *
from abjad.pitch import *
from abjad.scheme import *
from abjad.core import *
from abjad.segments import *
from abjad.spanners import *
from abjad.top import *

# import all the way down to module to satisfy mypy:
from abjad.mathtools import NonreducedFraction
from abjad.mathtools import NonreducedRatio
from abjad.mathtools import Ratio

# timespan classes and expression factory
from abjad.timespans import AnnotatedTimespan
from abjad.timespans import Timespan
from abjad.timespans import timespan
from abjad.timespans import TimespanList

# import version information
from ._version import __version_info__, __version__

from abjad import cli
from abjad import demos
from abjad import ly
from abjad import utilities

# singletons
tags = system.Tags()
