import math


def partition_sequence_extended_to_counts(sequence, counts, overhang=True):
    '''.. versionadded:: 2.0

    Partition sequence extended to counts.
    '''
    from abjad.tools import sequencetools

    n = int(math.ceil(float(sum(counts)) / len(sequence)))

    sequence = sequencetools.repeat_sequence_n_times(sequence, n)

    return sequencetools.partition_sequence_by_counts(sequence, counts, cyclic=False, overhang=overhang)
