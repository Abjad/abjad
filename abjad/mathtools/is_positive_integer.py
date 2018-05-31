import numbers


def is_positive_integer(argument):
    """
    Is true when ``argument`` equals a positive integer.

    ..  container:: example

        >>> abjad.mathtools.is_positive_integer(99)
        True

        >>> abjad.mathtools.is_positive_integer(0)
        False

        >>> abjad.mathtools.is_positive_integer(-1)
        False

    Returns true or false.
    """
    if isinstance(argument, numbers.Number):
        if argument == int(argument):
            if 0 < argument:
                return True
    return False
