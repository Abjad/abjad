# -*- encoding: utf-8 -*-


def diatonic_pitch_class_number_to_diatonic_pitch_class_name(diatonic_pitch_class_number):
    '''Change `diatonic_pitch_class_number` to diatonic pitch-class name:

    ::

        >>> pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name(0)
        'c'

    Return string.
    '''
    from abjad.tools import pitchtools
    try:
        return pitchtools.PitchClass._diatonic_pitch_class_number_to_diatonic_pitch_class_name[
            diatonic_pitch_class_number]
    except KeyError:
        raise ValueError('Not diatonic pitch-class number: {!r}.'.format(
            diatonic_pitch_class_number))
