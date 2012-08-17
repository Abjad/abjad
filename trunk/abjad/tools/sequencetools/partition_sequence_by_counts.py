from abjad.tools import mathtools
import copy


def partition_sequence_by_counts(sequence, counts, cyclic=False, overhang=False, copy_elements=False):
    '''.. versionadded:: 1.1

    Partition sequence by counts:

        >>> sequencetools.partition_sequence_by_counts(range(10), [3])
        [[0, 1, 2]]

    Partition sequence cyclically by count:

        >>> sequencetools.partition_sequence_by_counts(range(10), [3], cyclic=True)
        [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    Partition sequence by count with overhang:

        >>> sequencetools.partition_sequence_by_counts(range(10), [3], overhang=True)
        [[0, 1, 2], [3, 4, 5, 6, 7, 8, 9]]

    Partition sequence cyclically by count with overhang:

        >>> sequencetools.partition_sequence_by_counts(
        ...     range(10), [3], cyclic=True, overhang=True)
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    Partition sequence once by counts:

        >>> sequencetools.partition_sequence_by_counts(range(16), [4, 3])
        [[0, 1, 2, 3], [4, 5, 6]]

    Partition sequence cyclically by counts:

        >>> sequencetools.partition_sequence_by_counts(range(16), [4, 3], cyclic=True)
        [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13]]

    Partition sequence by counts with overhang:

        >>> sequencetools.partition_sequence_by_counts(range(16), [4, 3], overhang=True)
        [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10, 11, 12, 13, 14, 15]]

    Partition sequence cyclically by counts with overhang:

        >>> sequencetools.partition_sequence_by_counts(
        ...     range(16), [4, 3], cyclic=True, overhang=True)
        [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13], [14, 15]]

    Return list of sequence types.
    '''
    from abjad.tools import sequencetools

    assert sequencetools.all_are_nonnegative_integers(counts)

    result = []

    if cyclic:
        if overhang:
            counts = sequencetools.repeat_sequence_to_weight_exactly(counts, len(sequence))
        else:
            counts = sequencetools.repeat_sequence_to_weight_at_most(counts, len(sequence))
    elif overhang:
        weight_counts = mathtools.weight(counts)
        len_sequence = len(sequence)
        if weight_counts < len_sequence:
            counts = list(counts)
            counts.append(len(sequence) - weight_counts)

    for start, stop in mathtools.cumulative_sums_zero_pairwise(counts):
        result.append(type(sequence)(sequence[start:stop]))

    return result
