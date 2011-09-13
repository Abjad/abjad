from abjad.tools.pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name import chromatic_pitch_class_number_to_chromatic_pitch_class_name
from abjad.tools.pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats import chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats
from abjad.tools.pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps import chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps
import math


# TODO: write tests.

def chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(chromatic_pitch_number, accidental_spelling = 'mixed'):
    '''.. versionadded: 1.1.1

    Change `chromatic_pitch_number` to diatonic pitch-class name / alphabetic
    accidental abbreviation / octave number triple::

        abjad> pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(13, accidental_spelling = 'sharps')
        ('c', 's', 5)

    Return tuple.

    .. versionchanged:: 2.0
        renamed ``pitchtools.number_to_letter_accidental_octave()`` to
        ``pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple()``.
    '''

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
        pitch_name = chromatic_pitch_class_number_to_chromatic_pitch_class_name(pc)
    elif accidental_spelling == 'sharps':
        pitch_name = chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps(pc)
    elif accidental_spelling == 'flats':
        pitch_name = chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats(pc)
    else:
        raise ValueError('unknown accidental spelling.')

    # disassemble pitch name into letter and accidental
    letter = pitch_name[0]
    accidental = pitch_name[1:]

    # find octave
    octave = int(math.floor(chromatic_pitch_number / 12)) + 4

    # return uninque letter, accidental, octave triple
    return letter, accidental, octave
