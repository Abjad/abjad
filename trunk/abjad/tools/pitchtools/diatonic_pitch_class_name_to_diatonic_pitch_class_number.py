# -*- encoding: utf-8 -*-


def diatonic_pitch_class_name_to_diatonic_pitch_class_number(diatonic_pitch_class_name):
    '''Change `diatonic_pitch_class_name` to diatonic pitch-class number:

    ::

        >>> pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number('c')
        0

    Return integer.
    '''
    from abjad.tools import pitchtools
    try:
        return pitchtools.PitchClass._diatonic_pitch_class_name_to_diatonic_pitch_class_number[
            diatonic_pitch_class_name]
    except KeyError:
        raise ValueError(
            'Not a diatonic pitch-class name: {!r}.'.format(
                diatonic_pitch_class_name))
