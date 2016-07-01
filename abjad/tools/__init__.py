# -*- coding: utf-8 -*-
import six
from abjad.tools import systemtools
from abjad.tools import datastructuretools
#from abjad.tools import mathtools

# load constants into __builtins__ namespace
if six.PY3:
    import builtins
else:
    import __builtin__ as builtins
builtins.Less = datastructuretools.OrdinalConstant('value', -1, 'Less')
builtins.More = datastructuretools.OrdinalConstant('value', 1, 'More')
builtins.Exact = datastructuretools.OrdinalConstant('value', 0, 'Exact')
builtins.Left = datastructuretools.OrdinalConstant('x', -1, 'Left')
builtins.Right = datastructuretools.OrdinalConstant('x', 1, 'Right')
builtins.Center = datastructuretools.OrdinalConstant('y', 0, 'Center')
builtins.Up = datastructuretools.OrdinalConstant('y', 1, 'Up')
builtins.Down = datastructuretools.OrdinalConstant('y', -1, 'Down')
from abjad.tools import mathtools
builtins.Infinity = mathtools.Infinity()
builtins.NegativeInfinity = mathtools.NegativeInfinity()
del(builtins)
del(six)

systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    delete_systemtools=False,
    ignored_names=['abjadbooktools'],
    )