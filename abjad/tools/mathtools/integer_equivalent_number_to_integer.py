# -*- coding: utf-8 -*-
import numbers


def integer_equivalent_number_to_integer(number):
    '''Integer-equivalent `number` to integer.

    ::

        >>> mathtools.integer_equivalent_number_to_integer(17.0)
        17

    Returns noninteger-equivalent number unchanged:

    ::

        >>> mathtools.integer_equivalent_number_to_integer(17.5)
        17.5

    Raises type error on nonnumber input.

    Returns number.
    '''
    from abjad.tools import mathtools

    if not isinstance(number, numbers.Number):
        message = 'must be number: {!r}.'
        message = message.format(number)
        raise TypeError(message)

    if mathtools.is_integer_equivalent_number(number):
        return int(number)
    else:
        return number
