import numbers


def is_nonnegative_integer(argument):
    """
    Is true when ``argument`` equals a nonnegative integer.

    ..  container:: example

        >>> abjad.mathtools.is_nonnegative_integer(99)
        True

        >>> abjad.mathtools.is_nonnegative_integer(0)
        True

        >>> abjad.mathtools.is_nonnegative_integer(-1)
        False

    Returns true or false.
    """
    if isinstance(argument, numbers.Number):
        if argument == int(argument):
            if 0 <= argument:
                return True
    return False
