from abjad.tools import mathtools
from abjad.tools.sequencetools._split_sequence_by_weights import _split_sequence_by_weights
from abjad.tools.sequencetools.repeat_sequence_n_times import repeat_sequence_n_times
import math


def _split_sequence_extended_to_weights(sequence, weights, overhang = True):
    '''.. versionadded:: 2.0

    Split sequence extended to weights.
    '''

    n = int(math.ceil(float(mathtools.weight(weights)) / mathtools.weight(sequence)))

    sequence = repeat_sequence_n_times(sequence, n)

    return _split_sequence_by_weights(sequence, weights, cyclic = False, overhang = overhang)
