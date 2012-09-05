import fractions


def is_duration_pair(arg):
    '''.. versionadded:: 1.1

    True when `arg` has the form of a pair of integers that initialize a positive rational::

        >>> from abjad.tools import durationtools

    ::

        >>> durationtools.is_duration_pair((5, 16))
        True

    Otherwise false::

        >>> durationtools.is_duration_pair((-5, 16))
        False

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``durationtools.is_pair()`` to ``durationtools.is_duration_pair()``.
    '''

    if isinstance(arg, (list, tuple)) and len(arg) != 2:
        return False

    try:
        arg = fractions.Fraction(*arg)
    except:
        return False

    if 0 < arg:
        return True
    else:
        return False
