# -*- encoding: utf-8 -*-
# TODO: implement subsegment containment on pitchtools Segment classes
def contains_subsegment(pitch_class_numbers, pitch_numbers):
    '''True when `pitch_numbers` contain `pitch_class_numbers`
    as subsegment:

    ::

        >>> pcs = [2, 7, 10]
        >>> pitches = [6, 9, 12, 13, 14, 19, 22, 27, 28, 29, 32, 35]
        >>> pitchtools.contains_subsegment(pcs, pitches)
        True

    Returns boolean.
    '''

    pcs_start_index = [p % 12 for p in pitch_numbers].index(
        pitch_class_numbers[0] % 12)
    pcs_transposition = pitch_numbers[pcs_start_index] - pitch_class_numbers[0]
    transposed_pcs = [p + pcs_transposition for p in pitch_class_numbers]
    return set(transposed_pcs).issubset(set(pitch_numbers))
