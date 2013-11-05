# -*- encoding: utf-8 -*-
from abjad.tools.sequencetools.iterate_sequence_pairwise_strict \
	import iterate_sequence_pairwise_strict


def count_length_two_runs_in_sequence(sequence):
    '''Count length-``2`` runs in `sequence`:

    ::

        >>> sequencetools.count_length_two_runs_in_sequence([0, 0, 1, 1, 1, 2, 3, 4, 5])
        3

    Returns nonnegative integer.
    '''

    total_repetitions = 0
    for left, right in iterate_sequence_pairwise_strict(sequence):
        if left == right:
            total_repetitions += 1

    return total_repetitions
