# -*- encoding: utf-8 -*-


def pitch_number_to_pitch_name(
    pitch_number, accidental_spelling='mixed'):
    '''Change `pitch_number` to chromatic pitch name:

    ::

        >>> pitchtools.pitch_number_to_pitch_name(13)
        "cs''"

    Return string.
    '''
    from abjad.tools import pitchtools

    if not pitchtools.Pitch.is_pitch_number(pitch_number):
        raise ValueError('\n\tNot chromatic pitch number: '
            '{!r}'.format(pitch_number))

    if not isinstance(accidental_spelling, str):
        raise TypeError

    if not accidental_spelling in ('mixed', 'flats', 'sharps'):
        raise ValueError

    pitch_class_number = pitch_number % 12

    if accidental_spelling == 'mixed':
        pitch_class_name = pitchtools.pitch_class_number_to_pitch_class_name(
            pitch_class_number)
    elif accidental_spelling == 'sharps':
        pitch_class_name = \
            pitchtools.pitch_class_number_to_pitch_class_name_with_sharps(
            pitch_class_number)
    elif accidental_spelling == 'flats':
        pitch_class_name = \
            pitchtools.pitch_class_number_to_pitch_class_name_with_flats(
            pitch_class_number)
    else:
        raise ValueError('unknown accidental spelling: '
            '{!r}'.format(accidental_spelling))

    octave_number = pitch_number // 12 + 4
    octave_tick_string = str(pitchtools.OctaveIndication(octave_number))

    pitch_name = pitch_class_name + octave_tick_string

    return pitch_name
