from abjad.tools.pitchtools.Accidental import Accidental
from abjad.tools.pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number import diatonic_pitch_class_name_to_diatonic_pitch_class_number
from abjad.tools.pitchtools.diatonic_pitch_class_number_to_chromatic_pitch_class_number import diatonic_pitch_class_number_to_chromatic_pitch_class_number
from abjad.tools.pitchtools.is_chromatic_pitch_class_name import chromatic_pitch_class_name_regex


def chromatic_pitch_class_name_to_chromatic_pitch_class_number(chromatic_pitch_class_name):
    '''.. versionadded:: 2.0

    Change `chromatic_pitch_class_name` to chromatic pitch-class number::

        abjad> pitchtools.chromatic_pitch_class_name_to_chromatic_pitch_class_number('cs')
        1

    Return chromatic pitch-class number.
    '''

    match = chromatic_pitch_class_name_regex.match(chromatic_pitch_class_name)
    if match is None:
        raise ValueError('\n\tNot chromatic pitch-class name: "%s".' % chromatic_pitch_class_name)

    diatonic_pitch_class_name, alphabetic_accidental_abbreviation = match.groups()
    diatonic_pitch_class_number = diatonic_pitch_class_name_to_diatonic_pitch_class_number(
        diatonic_pitch_class_name)
    chromatic_pitch_class_number = diatonic_pitch_class_number_to_chromatic_pitch_class_number(
        diatonic_pitch_class_number)
    accidental = Accidental(alphabetic_accidental_abbreviation)
    chromatic_pitch_class_number += accidental.semitones
    chromatic_pitch_class_number %= 12

    return chromatic_pitch_class_number
