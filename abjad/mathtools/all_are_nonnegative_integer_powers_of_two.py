def all_are_nonnegative_integer_powers_of_two(argument):
    """
    Is true when ``argument`` is an iterable collection of nonnegative
    integer powers of two.

    ..  container:: example

        >>> items = [0, 1, 1, 1, 2, 4, 32, 32]
        >>> abjad.mathtools.all_are_nonnegative_integer_powers_of_two(items)
        True

        >>> abjad.mathtools.all_are_nonnegative_integer_powers_of_two(17)
        False

    ..  container:: example

        Is true when ``argument`` is empty:

        >>> abjad.mathtools.all_are_nonnegative_integer_powers_of_two([])
        True

    Returns true or false.
    """
    from abjad import mathtools
    try:
        return all(
            mathtools.is_nonnegative_integer_power_of_two(_)
            for _ in argument
            )
    except TypeError:
        return False
