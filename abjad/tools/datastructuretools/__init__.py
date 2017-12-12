import six
from abjad.tools import mathtools
from .OrdinalConstant import OrdinalConstant
if six.PY3:
    import builtins
else:
    import __builtin__ as builtins
builtins.Identity = OrdinalConstant('identity', 0, 'Identity')
builtins.Less = OrdinalConstant('value', -1, 'Less')
builtins.More = OrdinalConstant('value', 1, 'More')
builtins.Exact = OrdinalConstant('value', 0, 'Exact')
builtins.Left = OrdinalConstant('x', -1, 'Left')
builtins.Right = OrdinalConstant('x', 1, 'Right')
builtins.Both = OrdinalConstant('x', 0, 'Both')
builtins.Center = OrdinalConstant('y', 0, 'Center')
builtins.Up = OrdinalConstant('y', 1, 'Up')
builtins.Down = OrdinalConstant('y', -1, 'Down')
builtins.Top = OrdinalConstant('y', 1, 'Top')
builtins.Bottom = OrdinalConstant('y', -1, 'Bottom')
builtins.Infinity = mathtools.Infinity()
builtins.NegativeInfinity = mathtools.NegativeInfinity()
del(builtins)
del(six)
del(mathtools)

from .OrdinalConstant import OrdinalConstant
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
