import numbers


def is_integer_equivalent_number(argument):
    """
    Is true when ``argument`` is a number and ``argument`` is equivalent to an
    integer.

    ..  container:: example

        >>> abjad.mathtools.is_integer_equivalent_number(12.0)
        True

        >>> abjad.mathtools.is_integer_equivalent_number(abjad.Duration(1, 2))
        False

    Returns true or false.
    """
    if isinstance(argument, numbers.Number):
        if int(argument) == argument:
            return True
    return False
