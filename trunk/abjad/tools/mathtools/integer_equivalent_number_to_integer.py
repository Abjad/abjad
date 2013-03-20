import numbers


def integer_equivalent_number_to_integer(number):
    '''.. versionadded:: 2.0

    Integer-equivalent `number` to integer:

    ::

        >>> mathtools.integer_equivalent_number_to_integer(17.0)
        17

    Return noninteger-equivalent number unchanged:

    ::

        >>> mathtools.integer_equivalent_number_to_integer(17.5)
        17.5

    Raise type error on nonnumber input.

    Return number.
    '''
    from abjad.tools import mathtools

    if not isinstance(number, numbers.Number):
        raise TypeError('input "%s"% must be number.' % number)

    if mathtools.is_integer_equivalent_number(number):
        return int(number)
    else:
        return number
