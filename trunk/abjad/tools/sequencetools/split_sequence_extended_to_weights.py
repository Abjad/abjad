from abjad.tools import mathtools
import math


def split_sequence_extended_to_weights(sequence, weights, overhang=True):
    '''.. versionadded:: 2.0

    Split sequence extended to weights.
    '''
    from abjad.tools import sequencetools

    n = int(math.ceil(float(mathtools.weight(weights)) / mathtools.weight(sequence)))

    sequence = sequencetools.repeat_sequence_n_times(sequence, n)

    return sequencetools.split_sequence_by_weights(sequence, weights, cyclic=False, overhang=overhang)
