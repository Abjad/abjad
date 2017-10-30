def is_nonnegative_integer_equivalent_number(argument):
    '''Is true when `argument` is a nonnegative integer-equivalent number.
    Otherwise false.

    ..  container:: example

        >>> duration = abjad.Duration(4, 2)
        >>> abjad.mathtools.is_nonnegative_integer_equivalent_number(duration)
        True

    Returns true or false.
    '''
    from abjad.tools import mathtools
    return mathtools.is_integer_equivalent_number(argument) and 0 <= argument
