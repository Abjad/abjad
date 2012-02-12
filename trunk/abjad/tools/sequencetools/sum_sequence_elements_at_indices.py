from fractions import Fraction


def sum_sequence_elements_at_indices(sequence, pairs, period = None, overhang = True):
    '''.. versionadded:: 1.1

    Sum `sequence` elements at indices according to `pairs`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.sum_sequence_elements_at_indices(range(10), [(0, 3)])
        [3, 3, 4, 5, 6, 7, 8, 9]

    Sum `sequence` elements cyclically at indices according to `pairs` and `period`::

        abjad> sequencetools.sum_sequence_elements_at_indices(range(10), [(0, 3)], period = 4)
        [3, 3, 15, 7, 17]

    Sum `sequence` elements cyclically at indices according to `pairs` and `period`
    and do not return incomplete final sum::

        abjad> sequencetools.sum_sequence_elements_at_indices(range(10), [(0, 3)], period = 4, overhang = False)
        [3, 3, 15, 7]

    Replace ``sequence[i:i+count]`` with ``sum(sequence[i:i+count])``
    for each ``(i, count)`` in `pairs`.

    Indices in `pairs` must be less than `period` when `period` is not none.

    Return new list.

    .. versionchanged:: 2.0
        renamed ``sequencetools.sum_slices_at()`` to
        ``sequencetools.sum_sequence_elements_at_indices()``.
    '''

    assert isinstance(sequence, list)
    assert all([isinstance(x, (int, float, Fraction)) for x in sequence])
    assert isinstance(period, (int, type(None)))
    assert isinstance(overhang, bool)

    if not _check_sum_slices_at_specification(pairs):
        raise ValueError('must be list of nonoverlapping pairs.')

    start_indices = set([pair[0] for pair in pairs])
    indices_affected = []
    for pair in pairs:
        indices_affected.extend(range(pair[0], sum(pair)))

    if period is not None:
        if not max(indices_affected) < period:
            raise ValueError('affected indices must be less than period of repetition.')
    else:
        period = len(sequence)

    result = []
    slice_remaining = 0
    slice_total = None
    for i, x in enumerate(sequence):
        if i % period in start_indices:
            index, length = [pair for pair in pairs if pair[0] == i % period][0]
            slice_remaining = length
        if 0 < slice_remaining:
            if slice_total is None:
                slice_total = x
            else:
                slice_total += x
            slice_remaining -= 1

        if slice_remaining == 0:
            if slice_total is not None:
                result.append(slice_total)
                slice_total = None
            else:
                result.append(x)

    if 0 < slice_total:
        if overhang:
            result.append(slice_total)

    return result


def _check_sum_slices_at_specification(pairs):
    try:
        assert isinstance(pairs, list)
        assert all([isinstance(x, tuple) and len(x) == 2 and 0 < x[-1]
            for x in pairs])
        indices_affected = []
        for pair in pairs:
            indices_affected.extend(range(pair[0], sum(pair)))
        assert len(indices_affected) == len(set(indices_affected))
    except AssertionError:
        return False
    return True
