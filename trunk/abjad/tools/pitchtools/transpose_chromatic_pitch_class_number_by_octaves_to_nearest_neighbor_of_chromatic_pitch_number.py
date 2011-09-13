def transpose_chromatic_pitch_class_number_by_octaves_to_nearest_neighbor_of_chromatic_pitch_number(
    chromatic_pitch_number, chromatic_pitch_class_number):
    '''.. versionadded:: 1.1

    Transpose `chromatic_pitch_class_number` by octaves to nearest neighbor
    of `chromatic_pitch_number`::

        abjad> pitchtools.transpose_chromatic_pitch_class_number_by_octaves_to_nearest_neighbor_of_chromatic_pitch_number(12, 4)
        16

    Resulting chromatic pitch number must be within one tritone of `pitch_number`.

    Return integer or float.

    .. versionchanged:: 2.0
        renamed ``pitchtools.nearest_neighbor()`` to
        ``pitchtools.transpose_chromatic_pitch_class_number_by_octaves_to_nearest_neighbor_of_chromatic_pitch_number()``.
    '''

    target_pc = chromatic_pitch_number % 12
    down = (target_pc - chromatic_pitch_class_number) % 12
    up = (chromatic_pitch_class_number - target_pc) % 12
    if up < down:
        return chromatic_pitch_number + up
    else:
        return chromatic_pitch_number - down
