# -*- encoding: utf-8 -*-
import types
from abjad.tools import selectiontools


def all_are_components(expr, component_classes=None):
    '''True when elements in `expr` are all components:

    ::

        >>> componenttools.all_are_components(3 * Note("c'4"))
        True

    Otherwise false:

    ::

        >>> componenttools.all_are_components(['foo', 'bar'])
        False

    True when elements in `expr` are all `component_classes`:

    ::

        >>> componenttools.all_are_components(3 * Note("c'4"), component_classes=Note)
        True

    Otherwise false:

    ::

        >>> componenttools.all_are_components(['foo', 'bar'], component_classes=Note)
        False

    Return boolean.
    '''
    from abjad.tools import componenttools

    allowable = (list, tuple, types.GeneratorType, selectiontools.Selection)
    if not isinstance(expr, allowable):
        return False

    if component_classes is None:
        component_classes = componenttools.Component

    for element in expr:
        if not isinstance(element, component_classes):
            return False

    return True
