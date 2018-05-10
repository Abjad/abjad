from .OrdinalConstant import OrdinalConstant

from abjad.tools import mathtools  # noqa
Infinity = mathtools.Infinity()
NegativeInfinity = mathtools.NegativeInfinity()
del mathtools

from .CyclicTuple import CyclicTuple
from .Duration import Duration
from .Inequality import Inequality
from .DurationInequality import DurationInequality
from .Enumeration import Enumeration
from .Expression import Expression
from .LengthInequality import LengthInequality
from .Multiplier import Multiplier
from .Offset import Offset
from .Pattern import Pattern
from .TypedCollection import TypedCollection
from .TypedTuple import TypedTuple
from .OrderedDict import OrderedDict
from .PatternTuple import PatternTuple
from .PitchInequality import PitchInequality
from .Sequence import Sequence
from .SortedCollection import SortedCollection
from .String import String
from .TypedCounter import TypedCounter
from .TypedFrozenset import TypedFrozenset
from .TypedList import TypedList

_documentation_section = 'core'
