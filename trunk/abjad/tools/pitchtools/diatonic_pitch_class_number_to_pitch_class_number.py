# -*- encoding: utf-8 -*-


def diatonic_pitch_class_number_to_pitch_class_number(diatonic_pitch_class_number):
    '''Change `diatonic_pitch_class_number` to chromatic pitch-class number:

    ::

        >>> pitchtools.diatonic_pitch_class_number_to_pitch_class_number(6)
        11

    Return nonnegative integer.
    '''
    from abjad.tools import pitchtools
    try:
        return pitchtools.PitchClass._diatonic_pitch_class_number_to_pitch_class_number[
            diatonic_pitch_class_number]
    except KeyError:
        raise ValueError(
            'Not a diatonic pitch-class number: {!r}.'.format(
                diatonic_pitch_class_number))
