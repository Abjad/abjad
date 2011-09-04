from abjad.tools.sequencetools._partition_sequence_elements_by_weights_at_most import _partition_sequence_elements_by_weights_at_most


def partition_sequence_cyclically_by_weights_at_most_without_overhang(sequence, weights):
    '''.. versionadded:: 1.1

    Partition `sequence` elements cyclically by `weights` at most without overhang::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequence = [3, 3, 3, 3, 4, 4, 4, 4, 5]
        abjad> sequencetools.partition_sequence_cyclically_by_weights_at_most_without_overhang(sequence, [10, 5])
        [[3, 3, 3], [3], [4, 4], [4]]

    Return list sequence element reference lists.

    .. versionchanged:: 2.0
        renamed ``sequencetools.group_sequence_elements_cyclically_by_weights_at_most_without_overhang()`` to
        ``sequencetools.partition_sequence_cyclically_by_weights_at_most_without_overhang()``.
    '''

    return _partition_sequence_elements_by_weights_at_most(
        sequence, weights, cyclic = True, overhang = False)
