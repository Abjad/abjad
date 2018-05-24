import collections


def cumulative_products(argument):
    """
    Gets cumulative products of ``argument``.

    ..  container:: example

        >>> abjad.mathtools.cumulative_products([1, 2, 3, 4, 5, 6, 7, 8])
        [1, 2, 6, 24, 120, 720, 5040, 40320]

        >>> abjad.mathtools.cumulative_products([1, -2, 3, -4, 5, -6, 7, -8])
        [1, -2, -6, 24, 120, -720, -5040, 40320]

    Raises exception when ``argument`` is not iterable.

    Returns new object of ``argument`` type.
    """
    if not isinstance(argument, collections.Iterable):
        raise TypeError(argument)
    if len(argument) == 0:
        return type(argument)([])
    result = [argument[0]]
    for element in argument[1:]:
        result.append(result[-1] * element)
    return type(argument)(result)
