def all_are_integer_equivalent(argument):
    """
    Is true when ``argument`` is an iterable collection with
    integer-equivalent items.

    ..  container:: example

        >>> items = [1, '2', 3.0, abjad.Fraction(4, 1)]
        >>> abjad.mathtools.all_are_integer_equivalent(items)
        True

        >>> abjad.mathtools.all_are_integer_equivalent([1, '2', 3.5, 4])
        False

    Returns true or false.
    """
    from abjad import mathtools
    try:
        return all(
            mathtools.is_integer_equivalent(_)
            for _ in argument
            )
    except TypeError:
        return False
