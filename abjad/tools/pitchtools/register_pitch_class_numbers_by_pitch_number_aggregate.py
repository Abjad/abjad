# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools


def register_pitch_class_numbers_by_pitch_number_aggregate(
    pitch_class_numbers, aggregate):
    '''Register `pitch_class_numbers` by pitch-number `aggregate`:

    ::

        >>> pitchtools.register_pitch_class_numbers_by_pitch_number_aggregate(
        ...     [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11],
        ...     [10, 19, 20, 23, 24, 26, 27, 29, 30, 33, 37, 40])
        [10, 24, 26, 30, 20, 19, 29, 27, 37, 33, 40, 23]

    Returns list of zero or more pitch numbers.
    '''

    if isinstance(pitch_class_numbers, list):
        result = [
            [p for p in aggregate if p % 12 == pc] for pc in [x % 12 for x in pitch_class_numbers]]
        result = sequencetools.flatten_sequence(result)
    elif isinstance(pitch_class_numbers, int):
        result = [p for p in aggregate if p % 12 == pitch_class_numbers][0]
    else:
        message = 'must be pitch-class number or list of pitch-class numbers.'
        raise TypeError(message)
    return result
