# -*- encoding: utf-8 -*-


def diatonic_pitch_name_to_pitch_class_name(diatonic_pitch_name):
    '''Change `diatonic_pitch_name` to chromatic pitch-class name:

    ::

        >>> pitchtools.diatonic_pitch_name_to_pitch_class_name("c''")
        'c'

    Return string.
    '''
    from abjad.tools import pitchtools

    chromatic_pitch_name = pitchtools.diatonic_pitch_name_to_chromatic_pitch_name(diatonic_pitch_name)

    return pitchtools.chromatic_pitch_name_to_pitch_class_name(chromatic_pitch_name)
