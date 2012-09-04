import types


def all_are_components(expr, klasses=None):
    '''.. versionadded:: 1.1

    True when elements in `expr` are all components::

        >>> componenttools.all_are_components(3 * Note("c'4"))
        True

    Otherwise false::

        >>> componenttools.all_are_components(['foo', 'bar'])
        False

    True when elements in `expr` are all `klasses`::

        >>> componenttools.all_are_components(3 * Note("c'4"), klasses = Note)
        True

    Otherwise false::

        >>> componenttools.all_are_components(['foo', 'bar'], klasses = Note)
        False

    Return boolean.
    '''
    from abjad.tools import componenttools

    if not isinstance(expr, (list, tuple, types.GeneratorType)):
        return False

    if klasses is None:
        klasses = componenttools.Component

    for element in expr:
        if not isinstance(element, klasses):
            return False

    return True
