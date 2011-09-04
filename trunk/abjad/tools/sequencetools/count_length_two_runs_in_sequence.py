from abjad.tools.sequencetools.iterate_sequence_pairwise_strict import iterate_sequence_pairwise_strict


def count_length_two_runs_in_sequence(sequence):
    '''.. versionadded:: 1.1

    Count length-``2`` runs in `sequence`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.count_length_two_runs_in_sequence([0, 0, 1, 1, 1, 2, 3, 4, 5])
        3

    Return nonnegative integer.

    .. versionchanged:: 2.0
        renamed ``sequencetools.count_repetitions()`` to
        ``sequencetools.count_length_two_runs_in_sequence()``.
    '''

    total_repetitions = 0
    for left, right in iterate_sequence_pairwise_strict(sequence):
        if left == right:
            total_repetitions += 1

    return total_repetitions
