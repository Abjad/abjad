from abjad.tools import mathtools


def all_are_nonnegative_integer_powers_of_two(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a sequence and all elements in `expr` are nonnegative integer powers of two::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.all_are_nonnegative_integer_powers_of_two([0, 1, 1, 1, 2, 4, 32, 32])
        True

    True when `expr` is an empty sequence::

        abjad> sequencetools.all_are_nonnegative_integer_powers_of_two([])
        True

    False otherwise::

        abjad> sequencetools.all_are_nonnegative_integer_powers_of_two(17)
        False

    Return boolean.
    '''

    try:
        return all([mathtools.is_nonnegative_integer_power_of_two(x) for x in expr])
    except TypeError:
        return False
