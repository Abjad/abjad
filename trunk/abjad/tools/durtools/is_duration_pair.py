from fractions import Fraction


def is_duration_pair(arg):
    '''.. versionadded:: 1.1.1

    True when `arg` has the form of a pair of integers that initialize a positive rational::

        abjad> from abjad.tools import durtools

    ::

        abjad> durtools.is_duration_pair((5, 16))
        True

    Otherwise false::

        abjad> durtools.is_duration_pair((-5, 16))
        False

    Return boolean.

    .. versionchanged:: 1.1.2
        renamed ``durtools.is_pair( )`` to ``durtools.is_duration_pair( )``.
    '''

    if isinstance(arg, (list, tuple)) and len(arg) != 2:
        return False

    try:
        arg = Fraction(*arg)
    except:
        return False

    if 0 < arg:
        return True
    else:
        return False
