def is_nonnegative_integer_equivalent_number(argument):
    """
    Is true when ``argument`` is a nonnegative integer-equivalent number.

    ..  container:: example

        >>> duration = abjad.Duration(4, 2)
        >>> abjad.mathtools.is_nonnegative_integer_equivalent_number(duration)
        True

    Returns true or false.
    """
    from abjad import mathtools
    return mathtools.is_integer_equivalent_number(argument) and 0 <= argument
