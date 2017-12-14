from abjad.tools import mathtools
from .OrdinalConstant import OrdinalConstant

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
del OrdinalConstant
