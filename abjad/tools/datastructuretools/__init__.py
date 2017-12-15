from .OrdinalConstant import OrdinalConstant

from abjad.tools import mathtools

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
from .PatternTuple import PatternTuple
from .PitchInequality import PitchInequality
from .Sequence import Sequence
from .SortedCollection import SortedCollection
from .String import String
from .TreeNode import TreeNode
from .TreeContainer import TreeContainer
from .TypedCounter import TypedCounter
from .TypedFrozenset import TypedFrozenset
from .TypedList import TypedList
from .TypedOrderedDict import TypedOrderedDict


_documentation_section = 'core'
