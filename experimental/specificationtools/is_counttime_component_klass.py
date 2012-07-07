from abjad.tools import containertools
from abjad.tools import leaftools
from abjad.tools import measuretools
from abjad.tools import tuplettools


def is_counttime_component_klass(expr):
    r'''.. versionadded:: 1.0

    True when `expr` is a subclass of ``Measure``, ``Tuplet`` or ``Leaf``.

    Also true when `expr` is ``Container``::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.is_counttime_component_class(tuplettools.Tuplet)
        True

    Otherwise false::

        >>> specificationtools.is_counttime_component_class(voicetools.Voice)
        False

    Return boolean.
    '''

    if issubclass(expr, (measuretools.Measure, tuplettools.Tuplet, leaftools.Leaf)):
        return True
    elif expr == containertools.Container:
        return True
    else:
        return False
