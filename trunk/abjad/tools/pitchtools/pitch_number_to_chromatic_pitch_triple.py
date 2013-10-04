# -*- encoding: utf-8 -*-
import math


# TODO: can't this just return a named chromatic pitch class instance?
def pitch_number_to_chromatic_pitch_triple(
    pitch_number, accidental_spelling='mixed'):
    '''Change `pitch_number` to diatonic pitch-class name / alphabetic
    accidental abbreviation / octave number triple:

    ::

        >>> pitchtools.pitch_number_to_chromatic_pitch_triple(
        ... 13, accidental_spelling='sharps')
        ('c', Accidental('s'), 5)

    Return tuple.
    '''
    from abjad.tools import pitchtools

    # check input
    if not isinstance(pitch_number, (int, long, float)):
        raise TypeError

    if not isinstance(accidental_spelling, str):
        raise TypeError

    if not accidental_spelling in ('mixed', 'flats', 'sharps'):
        raise ValueError

    # find pc
    pc = pitch_number % 12

    # find pitch name from pc according to accidental spelling
    if accidental_spelling == 'mixed':
        pitch_name = pitchtools.pitch_class_number_to_pitch_class_name(pc)
    elif accidental_spelling == 'sharps':
        pitch_name = pitchtools.pitch_class_number_to_pitch_class_name_with_sharps(pc)
    elif accidental_spelling == 'flats':
        pitch_name = pitchtools.pitch_class_number_to_pitch_class_name_with_flats(pc)
    else:
        raise ValueError('unknown accidental spelling.')

    # disassemble pitch name into letter and accidental
    letter = pitch_name[0]
    alphabetic_accidental_abbreviation = pitch_name[1:]
    accidental = pitchtools.Accidental(alphabetic_accidental_abbreviation)

    # find octave
    octave = int(math.floor(pitch_number / 12)) + 4

    # return uninque letter, accidental, octave triple
    return letter, accidental, octave
