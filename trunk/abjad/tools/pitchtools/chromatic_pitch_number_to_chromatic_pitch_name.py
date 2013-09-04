# -*- encoding: utf-8 -*-


def chromatic_pitch_number_to_chromatic_pitch_name(
    chromatic_pitch_number, accidental_spelling='mixed'):
    '''Change `chromatic_pitch_number` to chromatic pitch name:

    ::

        >>> pitchtools.chromatic_pitch_number_to_chromatic_pitch_name(13)
        "cs''"

    Return string.
    '''
    from abjad.tools import pitchtools

    if not pitchtools.is_chromatic_pitch_number(chromatic_pitch_number):
        raise ValueError('\n\tNot chromatic pitch number: '
            '{!r}'.format(chromatic_pitch_number))

    if not isinstance(accidental_spelling, str):
        raise TypeError

    if not accidental_spelling in ('mixed', 'flats', 'sharps'):
        raise ValueError

    chromatic_pitch_class_number = chromatic_pitch_number % 12

    if accidental_spelling == 'mixed':
        chromatic_pitch_class_name = pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name(
            chromatic_pitch_class_number)
    elif accidental_spelling == 'sharps':
        chromatic_pitch_class_name = \
            pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps(
            chromatic_pitch_class_number)
    elif accidental_spelling == 'flats':
        chromatic_pitch_class_name = \
            pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats(
            chromatic_pitch_class_number)
    else:
        raise ValueError('unknown accidental spelling: '
            '{!r}'.format(accidental_spelling))

    octave_number = chromatic_pitch_number // 12 + 4
    octave_tick_string = str(pitchtools.OctaveIndication(octave_number))

    chromatic_pitch_name = chromatic_pitch_class_name + octave_tick_string

    return chromatic_pitch_name
