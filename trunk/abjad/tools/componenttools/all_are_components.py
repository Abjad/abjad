import types
from abjad.tools import selectiontools


def all_are_components(expr, classes=None):
    '''.. versionadded:: 1.1

    True when elements in `expr` are all components:

    ::

        >>> componenttools.all_are_components(3 * Note("c'4"))
        True

    Otherwise false:

    ::

        >>> componenttools.all_are_components(['foo', 'bar'])
        False

    True when elements in `expr` are all `classes`:

    ::

        >>> componenttools.all_are_components(3 * Note("c'4"), classes=Note)
        True

    Otherwise false:

    ::

        >>> componenttools.all_are_components(['foo', 'bar'], classes=Note)
        False

    Return boolean.
    '''
    from abjad.tools import componenttools

    allowable = (list, tuple, types.GeneratorType, selectiontools.SequentialSelection)
    if not isinstance(expr, allowable):
        return False

    if classes is None:
        classes = componenttools.Component

    for element in expr:
        if not isinstance(element, classes):
            return False

    return True
