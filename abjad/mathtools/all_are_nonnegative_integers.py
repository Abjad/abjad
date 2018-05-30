def all_are_nonnegative_integers(argument):
    """
    Is true when ``argument`` is an iterable collection of nonnegative
    integers.

    ..  container:: example

        >>> abjad.mathtools.all_are_nonnegative_integers([0, 1, 2, 99])
        True

        >>> abjad.mathtools.all_are_nonnegative_integers([0, 1, 2, -99])
        False

    Returns true or false.
    """
    from abjad import mathtools
    try:
        return all(mathtools.is_nonnegative_integer(_) for _ in argument)
    except TypeError:
        return False
