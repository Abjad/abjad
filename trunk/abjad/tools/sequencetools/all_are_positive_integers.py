from abjad.tools import mathtools


def all_are_positive_integers(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a sequence and all elements  in `expr` are positive integers::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.all_are_positive_integers([1, 2, 3, 99])
        True

    Otherwise false::

        abjad> sequencetools.all_are_positive_integers(17)
        False

    Return boolean.
    '''

    try:
        return all([mathtools.is_positive_integer(x) for x in expr])
    except TypeError:
        return False
