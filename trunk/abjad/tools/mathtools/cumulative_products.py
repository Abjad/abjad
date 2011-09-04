def cumulative_products(sequence):
    '''Cumulative products of `sequence`::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.cumulative_products([1, 2, 3, 4, 5, 6, 7, 8])
        [1, 2, 6, 24, 120, 720, 5040, 40320]

    ::

        abjad> mathtools.cumulative_products([1, -2, 3, -4, 5, -6, 7, -8])
        [1, -2, -6, 24, 120, -720, -5040, 40320]

    Raise type error when `sequence` is neither list nor tuple.

    Raise value error on empty `sequence`.

    Return list.

    .. versionchanged:: 2.0
        renamed ``sequencetools.cumulative_products()`` to
        ``mathtools.cumulative_products()``.
    '''

    if not isinstance(sequence, (list, tuple)):
        raise TypeError

    if len(sequence) == 0:
        raise ValueError

    result = [sequence[0]]
    for element in sequence[1:]:
        result.append(result[-1] * element)

    return result
