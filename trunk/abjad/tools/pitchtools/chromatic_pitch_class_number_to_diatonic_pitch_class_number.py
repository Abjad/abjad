# -*- encoding: utf-8 -*-


def chromatic_pitch_class_number_to_diatonic_pitch_class_number(chromatic_pitch_class_number):
    '''Change `chromatic_pitch_class_number` to diatonic pitch-class number:

    ::

        >>> pitchtools.chromatic_pitch_class_number_to_diatonic_pitch_class_number(1)
        0

    Return integer.
    '''
    from abjad.tools import pitchtools

    pitch_class_name = pitchtools.chromatic_pitch_class_number_to_pitch_class_name(
        chromatic_pitch_class_number)

    diatonic_pitch_class_name = pitchtools.pitch_class_name_to_diatonic_pitch_class_name(
        pitch_class_name)

    return pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number(diatonic_pitch_class_name)
