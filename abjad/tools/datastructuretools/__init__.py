# -*- coding: utf-8 -*-
import six
from .OrdinalConstant import OrdinalConstant
# load constants into __builtins__ namespace
if six.PY3:
    import builtins
else:
    import __builtin__ as builtins
builtins.Identity = OrdinalConstant('value', 0, 'Identity')
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
from abjad.tools import mathtools
builtins.Infinity = mathtools.Infinity()
builtins.NegativeInfinity = mathtools.NegativeInfinity()
del(builtins)
del(six)


from abjad.tools import systemtools
systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )

_documentation_section = 'core'
