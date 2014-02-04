# -*- encoding: utf-8 -*-


def count_length_two_runs_in_sequence(sequence):
    '''Counts length-``2`` runs in `sequence`.

    ::

        >>> sequencetools.count_length_two_runs_in_sequence([0, 0, 1, 1, 1, 2, 3, 4, 5])
        3

    Returns nonnegative integer.
    '''
    from abjad.tools import sequencetools

    total_repetitions = 0
    pairs = sequencetools.iterate_sequence_pairwise_strict(sequence)
    for left, right in pairs:
        if left == right:
            total_repetitions += 1

    return total_repetitions
