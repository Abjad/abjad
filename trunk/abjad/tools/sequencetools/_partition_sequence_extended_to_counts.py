from abjad.tools.sequencetools._partition_sequence_by_counts import _partition_sequence_by_counts
from abjad.tools.sequencetools.repeat_sequence_n_times import repeat_sequence_n_times
import math


def _partition_sequence_extended_to_counts(sequence, counts, overhang = True):
    '''Partition sequence extended to counts.
    '''

    n = int(math.ceil(float(sum(counts)) / len(sequence)))

    sequence = repeat_sequence_n_times(sequence, n)

    return _partition_sequence_by_counts(sequence, counts, cyclic = False, overhang = overhang)
