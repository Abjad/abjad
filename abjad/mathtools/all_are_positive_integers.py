def all_are_positive_integers(argument):
    """
    Is true when ``argument`` is an iterable collection of positive integers.

    ..  container:: example

        >>> abjad.mathtools.all_are_positive_integers([1, 2, 3, 99])
        True

        >>> abjad.mathtools.all_are_positive_integers(17)
        False

    Returns true or false.
    """
    from abjad import mathtools
    try:
        return all(mathtools.is_positive_integer(_) for _ in argument)
    except TypeError:
        return False
