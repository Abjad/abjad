# -*- encoding: utf-8 -*-


def pitch_name_to_diatonic_pitch_class_name(pitch_name):
    '''Change `pitch_name` to diatonic pitch name:

    ::

        >>> pitchtools.pitch_name_to_diatonic_pitch_class_name("cs''")
        'c'

    Return string.
    '''
    from abjad.tools import pitchtools

    if not pitchtools.Pitch.is_pitch_name(pitch_name):
        raise ValueError('\n\tNote chromatic pitch name: "%s".' % pitch_name)

    return pitch_name[0]
