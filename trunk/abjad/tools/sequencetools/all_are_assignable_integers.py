from abjad.tools import mathtools


def all_are_assignable_integers(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a sequence and all elements in `expr` are notehead-assignable integers::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.all_are_assignable_integers([1, 2, 3, 4, 6, 7, 8, 12, 14, 15, 16])
        True

    True when `expr` is an empty sequence::

        abjad> sequencetools.all_are_assignable_integers([])
        True

    False otherwise::

        abjad> sequencetools.all_are_assignable_integers('foo')
        False

    Return boolean.
    '''

    try:
        return all([mathtools.is_assignable_integer(x) for x in expr])
    except TypeError:
        return False
