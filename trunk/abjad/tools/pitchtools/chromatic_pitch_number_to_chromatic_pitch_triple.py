import math


# TODO: can't this just return a named chromatic pitch class instance?
def chromatic_pitch_number_to_chromatic_pitch_triple(
    chromatic_pitch_number, accidental_spelling='mixed'):
    '''.. versionadded: 1.1.1

    Change `chromatic_pitch_number` to diatonic pitch-class name / alphabetic
    accidental abbreviation / octave number triple::

        >>> pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(
        ... 13, accidental_spelling='sharps')
        ('c', Accidental('s'), 5)

    Return tuple.

    .. versionchanged:: 2.0
        renamed ``pitchtools.number_to_letter_accidental_octave()`` to
        ``pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple()``.
    '''
    from abjad.tools import pitchtools

    # check input
    if not isinstance(chromatic_pitch_number, (int, long, float)):
        raise TypeError

    if not isinstance(accidental_spelling, str):
        raise TypeError

    if not accidental_spelling in ('mixed', 'flats', 'sharps'):
        raise ValueError

    # find pc
    pc = chromatic_pitch_number % 12

    # find pitch name from pc according to accidental spelling
    if accidental_spelling == 'mixed':
        pitch_name = pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name(pc)
    elif accidental_spelling == 'sharps':
        pitch_name = pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps(pc)
    elif accidental_spelling == 'flats':
        pitch_name = pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats(pc)
    else:
        raise ValueError('unknown accidental spelling.')

    # disassemble pitch name into letter and accidental
    letter = pitch_name[0]
    alphabetic_accidental_abbreviation = pitch_name[1:]
    accidental = pitchtools.Accidental(alphabetic_accidental_abbreviation)

    # find octave
    octave = int(math.floor(chromatic_pitch_number / 12)) + 4

    # return uninque letter, accidental, octave triple
    return letter, accidental, octave
