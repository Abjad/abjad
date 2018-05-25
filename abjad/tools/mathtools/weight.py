def weight(argument):
    """
    Gets weight of ``argument``.

    ..  container:: example

        >>> abjad.mathtools.weight([-1, -2, 3, 4, 5])
        15

    ..  container:: example

        >>> abjad.mathtools.weight([])
        0

    Defined equal to sum of the absolute value of items in ``argument``.

    Returns nonnegative integer.
    """
    return sum([abs(_) for _ in argument])
