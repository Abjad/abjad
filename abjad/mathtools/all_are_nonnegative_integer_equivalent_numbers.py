def all_are_nonnegative_integer_equivalent_numbers(argument):
    """
    Is true when ``argument`` is an iterable collection of nonnegative
    integer-equivalent numbers.

    ..  container:: example

        >>> items = [0, 0.0, abjad.Fraction(0), 2, 2.0, abjad.Fraction(2)]
        >>> abjad.mathtools.all_are_nonnegative_integer_equivalent_numbers(items)
        True

        >>> items = [0, 0.0, abjad.Fraction(0), -2, 2.0, abjad.Fraction(2)]
        >>> abjad.mathtools.all_are_nonnegative_integer_equivalent_numbers(items)
        False

    Returns true or false.
    """
    from abjad import mathtools
    try:
        return all(
            mathtools.is_nonnegative_integer_equivalent_number(_)
            for _ in argument
            )
    except TypeError:
        return False
