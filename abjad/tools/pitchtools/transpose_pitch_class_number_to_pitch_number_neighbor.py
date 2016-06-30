# -*- coding: utf-8 -*-


def transpose_pitch_class_number_to_pitch_number_neighbor(
    pitch_number, pitch_class_number):
    '''Transposes `pitch_class_number` by octaves to nearest neighbor
    of `pitch_number`.

    ::

        >>> pitchtools.transpose_pitch_class_number_to_pitch_number_neighbor(
        ...     12, 4)
        16

    Resulting pitch number must be within one tritone of `pitch_number`.

    Returns pitch number.
    '''

    target_pc = pitch_number % 12

    down = (target_pc - pitch_class_number) % 12
    up = (pitch_class_number - target_pc) % 12

    if up < down:
        return pitch_number + up
    else:
        return pitch_number - down