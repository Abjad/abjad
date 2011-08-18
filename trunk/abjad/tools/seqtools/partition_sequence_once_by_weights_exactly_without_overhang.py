from abjad.tools.seqtools._partition_sequence_elements_by_weights_exactly import _partition_sequence_elements_by_weights_exactly


def partition_sequence_once_by_weights_exactly_without_overhang(sequence, weights):
    '''.. versionadded:: 1.1

    Partition `sequence` elements once by `weights` exactly without overhang::

        abjad> from abjad.tools import seqtools

    ::

        abjad> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
        abjad> seqtools.partition_sequence_once_by_weights_exactly_without_overhang(sequence, [3, 9])
        [[3], [3, 3, 3]]

    Return list sequence element reference lists.

    .. versionchanged:: 2.0
        renamed ``seqtools.group_sequence_elements_once_by_weights_exactly_without_overhang()`` to
        ``seqtools.partition_sequence_once_by_weights_exactly_without_overhang()``.
    '''

    return _partition_sequence_elements_by_weights_exactly(
        sequence, weights, cyclic = False, overhang = False)
