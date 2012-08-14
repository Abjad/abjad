# TODO: implement subsegment containment on pitchtools ObjectSegment classes
def contains_subsegment(chromatic_pitch_class_numbers, chromatic_pitch_numbers):
    '''.. versionadded:: 1.1

    True when `chromatic_pitch_numbers` contain `chromatic_pitch_class_numbers`
    as subsegment::

        >>> pcs = [2, 7, 10]
        >>> pitches = [6, 9, 12, 13, 14, 19, 22, 27, 28, 29, 32, 35]
        >>> pitchtools.contains_subsegment(pcs, pitches)
        True

    Return boolean.
    '''

    pcs_start_index = [p % 12 for p in chromatic_pitch_numbers].index(
        chromatic_pitch_class_numbers[0] % 12)
    pcs_transposition = chromatic_pitch_numbers[pcs_start_index] - chromatic_pitch_class_numbers[0]
    transposed_pcs = [p + pcs_transposition for p in chromatic_pitch_class_numbers]
    return set(transposed_pcs).issubset(set(chromatic_pitch_numbers))
