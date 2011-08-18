from abjad.tools.seqtools._partition_sequence_elements_by_weights_at_most import _partition_sequence_elements_by_weights_at_most


def partition_sequence_once_by_weights_at_most_with_overhang(sequence, weights):
    '''.. versionadded:: 1.1

    Partition `sequence` elements once by `weights` at most with overhang::

        abjad> from abjad.tools import seqtools

    ::

        abjad> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
        abjad> seqtools.partition_sequence_once_by_weights_at_most_with_overhang(sequence, [10, 4])
        [[3, 3, 3], [3], [4, 4, 4, 4, 5, 5]]

    Return list sequence element reference lists.

    .. versionchanged:: 2.0
        renamed ``seqtools.group_sequence_elements_once_by_weights_at_most_with_overhang()`` to
        ``seqtools.partition_sequence_once_by_weights_at_most_with_overhang()``.
    '''

    return _partition_sequence_elements_by_weights_at_most(
        sequence, weights, cyclic = False, overhang = True)
