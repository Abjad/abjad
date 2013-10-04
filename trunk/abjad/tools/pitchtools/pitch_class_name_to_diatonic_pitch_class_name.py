# -*- encoding: utf-8 -*-


def pitch_class_name_to_diatonic_pitch_class_name(pitch_class_name):
    '''Change `pitch_class_name` to diatonic pitch-class name:

    ::

        >>> pitchtools.pitch_class_name_to_diatonic_pitch_class_name('cs')
        'c'

    Return string.
    '''

    return pitch_class_name[0]
