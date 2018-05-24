def difference_series(argument):
    """
    Gets difference series of ``argument``.

    ..  container:: example

        >>> abjad.mathtools.difference_series([1, 1, 2, 3, 5, 5, 6])
        [0, 1, 1, 2, 0, 1]

        >>> abjad.mathtools.difference_series([9, 6, 8, 5, 7, 4, 6])
        [-3, 2, -3, 2, -3, 2]

    Returns new object of ``argument`` type.
    """
    result = []
    for i, n in enumerate(argument[1:]):
        result.append(n - argument[i])
    return type(argument)(result)
