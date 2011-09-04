from abjad.tools.sequencetools._partition_sequence_elements_by_weights_exactly import _partition_sequence_elements_by_weights_exactly


def partition_sequence_once_by_weights_exactly_without_overhang(sequence, weights):
    '''.. versionadded:: 1.1

    Partition `sequence` elements once by `weights` exactly without overhang::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
        abjad> sequencetools.partition_sequence_once_by_weights_exactly_without_overhang(sequence, [3, 9])
        [[3], [3, 3, 3]]

    Return list sequence element reference lists.

    .. versionchanged:: 2.0
        renamed ``sequencetools.group_sequence_elements_once_by_weights_exactly_without_overhang()`` to
        ``sequencetools.partition_sequence_once_by_weights_exactly_without_overhang()``.
    '''

    return _partition_sequence_elements_by_weights_exactly(
        sequence, weights, cyclic = False, overhang = False)
