def partition_sequence_by_weights_exactly(sequence, weights, cyclic, overhang):
    r'''.. versionadded:: 1.1

    Partition `sequence` by `weights` exactly.
    '''
    from abjad.tools import sequencetools
    from abjad.tools.sequencetools.split_sequence_by_weights import split_sequence_by_weights

    candidate = split_sequence_by_weights(sequence, weights, cyclic=cyclic, overhang=overhang)
    flattened_candidate = sequencetools.flatten_sequence(candidate)
    if flattened_candidate == sequence[:len(flattened_candidate)]:
        return candidate
    else:
        raise PartitionError('can not partition exactly.')
