# -*- encoding: utf-8 -*-


def diatonic_pitch_class_name_to_pitch_class_number(diatonic_pitch_class_name):
    '''Change `diatonic_pitch_class_name` to chromatic pitch-class number:

    ::

        >>> pitchtools.diatonic_pitch_class_name_to_pitch_class_number('f')
        5

    Return integer.
    '''
    from abjad.tools import pitchtools
    return pitchtools.PitchClass._diatonic_pitch_class_name_to_pitch_class_number[
        diatonic_pitch_class_name]
