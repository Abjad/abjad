def is_integer_equivalent_n_tuple(argument, n):
    """
    Is true when ``argument`` is a tuple of ``n`` integer-equivalent items.

    ..  container:: example

        >>> tuple_ = (2.0, '3', abjad.Fraction(4, 1))
        >>> abjad.mathtools.is_integer_equivalent_n_tuple(tuple_, 3)
        True

        >>> tuple_ = (2.5, '3', abjad.Fraction(4, 1))
        >>> abjad.mathtools.is_integer_equivalent_n_tuple(tuple_, 3)
        False

    Returns true or false.
    """
    from abjad import mathtools
    return (
        isinstance(argument, tuple) and
        len(argument) == n and
        all(mathtools.is_integer_equivalent(_) for _ in argument)
        )
