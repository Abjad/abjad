from abjad.tools import containertools
from abjad.tools import leaftools
from abjad.tools import measuretools
from abjad.tools import tuplettools


def is_counttime_component_klass_expr(expr):
    r'''

    True when `expr` is a subclass of ``Measure``, ``Tuplet`` or ``Leaf``.

    True when `expr` is ``Container``.

    True when `expr` is a tuple of one or more of these.

        >>> from experimental.tools import *

    ::

        >>> helpertools.is_counttime_component_klass_expr(tuplettools.Tuplet)
        True

    Otherwise false::

        >>> helpertools.is_counttime_component_klass_expr(voicetools.Voice)
        False

    Return boolean.
    '''

    if isinstance(expr, tuple) and all([is_counttime_component_klass_expr(x) for x in expr]):
        return True
    elif issubclass(expr, (measuretools.Measure, tuplettools.Tuplet, leaftools.Leaf)):
        return True
    elif expr == containertools.Container:
        return True
    else:
        return False
