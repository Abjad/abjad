def transpose_chromatic_pitch_class_number_to_chromatic_pitch_number_neighbor(
    chromatic_pitch_number, chromatic_pitch_class_number):
    '''.. versionadded:: 1.1

    Transpose `chromatic_pitch_class_number` by octaves to nearest neighbor
    of `chromatic_pitch_number`::

        >>> pitchtools.transpose_chromatic_pitch_class_number_to_chromatic_pitch_number_neighbor(
        ...     12, 4)
        16

    Resulting chromatic pitch number must be within one tritone of `chromatic_pitch_number`.

    Return chromatic pitch number.
    '''

    target_pc = chromatic_pitch_number % 12

    down = (target_pc - chromatic_pitch_class_number) % 12
    up = (chromatic_pitch_class_number - target_pc) % 12

    if up < down:
        return chromatic_pitch_number + up
    else:
        return chromatic_pitch_number - down
