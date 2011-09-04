from abjad.tools import mathtools


def all_are_nonnegative_integers(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a sequence and all elements  in `expr` are nonnegative integers::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.all_are_nonnegative_integers([0, 1, 2, 99])
        True

    Otherwise false::

        abjad> sequencetools.all_are_nonnegative_integers([0, 1, 2, -99])
        False

    Return boolean.
    '''

    try:
        return all([mathtools.is_nonnegative_integer(x) for x in expr])
    except TypeError:
        return False
