def cumulative_sums_zero(sequence):
    '''Cumulative sums of `sequence` starting from ``0``::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.cumulative_sums_zero([1, 2, 3, 4, 5, 6, 7, 8])
        [0, 1, 3, 6, 10, 15, 21, 28, 36]

    Return ``[0]`` on empty `sequence`::

        abjad> mathtools.cumulative_sums_zero([])
        [0]

    Return list.

    .. versionchanged:: 2.0
        renamed ``mathtools.cumulative_sums_zero()`` to
        ``mathtools.cumulative_sums_zero()``.
    '''

    result = [0]
    for element in sequence:
        result.append(result[-1] + element)

    return result
