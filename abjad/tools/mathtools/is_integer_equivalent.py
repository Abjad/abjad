import numbers


def is_integer_equivalent(argument):
    '''Is true when `argument` is an integer-equivalent number. Otherwise
    false.

    ..  container:: example

        >>> abjad.mathtools.is_integer_equivalent(12.0)
        True

        >>> abjad.mathtools.is_integer_equivalent('12')
        True

        >>> abjad.mathtools.is_integer_equivalent('foo')
        False

    Returns true or false.
    '''
    from abjad.tools import mathtools
    if isinstance(argument, numbers.Number):
        return mathtools.is_integer_equivalent_number(argument)
    try:
        int(argument)
        return True
    except (TypeError, ValueError):
        return False
