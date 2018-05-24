def cumulative_sums(argument, start=0):
    """
    Gets cumulative sums of ``argument``.

    ..  container:: example

        >>> abjad.mathtools.cumulative_sums([1, 2, 3, 4, 5, 6, 7, 8], start=0)
        [0, 1, 3, 6, 10, 15, 21, 28, 36]

        >>> abjad.mathtools.cumulative_sums([1, 2, 3, 4, 5, 6, 7, 8], start=None)
        [1, 3, 6, 10, 15, 21, 28, 36]

    Raises exception when ``argument`` is not iterable.

    Returns new object of ``argument`` type.
    """
    if start is None:
        result = []
    else:
        result = [start]
    for item in argument:
        if result:
            new = result[-1] + item
            result.append(new)
        else:
            result.append(item)
    return type(argument)(result)
