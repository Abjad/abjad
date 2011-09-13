# TODO: extend function to work on Abjad pitch instances.
def ordered_chromatic_pitch_class_numbers_are_within_ordered_chromatic_pitch_numbers(
    chromatic_pitch_class_numbers, chromatic_pitch_numbers):
    '''.. versionadded:: 1.1

    True if ordered `chromatic_pitch_class_numbers`are within ordered `chromatic_pitch_numbers`::

        abjad> pcs = [2, 7, 10]
        abjad> pitches = [6, 9, 12, 13, 14, 19, 22, 27, 28, 29, 32, 35]
        abjad> pitchtools.ordered_chromatic_pitch_class_numbers_are_within_ordered_chromatic_pitch_numbers(pcs, pitches)
        True

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``pitchtools.are_in_octave_order()`` to
        ``pitchtools.ordered_chromatic_pitch_class_numbers_are_within_ordered_chromatic_pitch_numbers()``.
    '''

    pcs_start_index = [p % 12 for p in chromatic_pitch_numbers].index(
        chromatic_pitch_class_numbers[0] % 12)
    pcs_transposition = chromatic_pitch_numbers[pcs_start_index] - chromatic_pitch_class_numbers[0]
    transposed_pcs = [p + pcs_transposition for p in chromatic_pitch_class_numbers]
    return set(transposed_pcs).issubset(set(chromatic_pitch_numbers))
