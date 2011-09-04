from abjad.tools.sequencetools._partition_sequence_elements_by_weights_exactly import _partition_sequence_elements_by_weights_exactly


def partition_sequence_cyclically_by_weights_exactly_with_overhang(sequence, weights):
    '''.. versionadded:: 1.1

    Partition `sequence` elements cyclically by `weights` exactly with overhang::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5]
        abjad> sequencetools.partition_sequence_cyclically_by_weights_exactly_with_overhang(sequence, [12])
        [[3, 3, 3, 3], [4, 4, 4], [4, 5]]

    Return list of sequence element reference lists.

    .. versionchanged:: 2.0
        renamed ``sequencetools.group_sequence_elements_cyclically_by_weights_exactly_with_overhang()`` to
        ``sequencetools.partition_sequence_cyclically_by_weights_exactly_with_overhang()``.
    '''

    return _partition_sequence_elements_by_weights_exactly(
        sequence, weights, cyclic = True, overhang = True)
