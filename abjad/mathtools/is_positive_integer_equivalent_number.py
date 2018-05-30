def is_positive_integer_equivalent_number(argument):
    """
    Is true when ``argument`` is a positive integer-equivalent number.

    ..  container:: example

        >>> abjad.mathtools.is_positive_integer_equivalent_number(
        ...     abjad.Duration(4, 2)
        ...     )
        True

    Returns true or false.
    """
    from abjad import mathtools
    try:
        return (
            0 < argument and
            mathtools.is_integer_equivalent_number(argument)
            )
    except TypeError:  # Python 3 comparisons with non-numbers
        return False
