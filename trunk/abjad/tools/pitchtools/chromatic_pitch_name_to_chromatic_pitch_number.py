from abjad.tools.pitchtools.Accidental import Accidental
from abjad.tools.pitchtools.chromatic_pitch_class_name_to_chromatic_pitch_class_number import chromatic_pitch_class_name_to_chromatic_pitch_class_number
from abjad.tools.pitchtools.diatonic_pitch_class_name_to_diatonic_pitch_class_number import diatonic_pitch_class_name_to_diatonic_pitch_class_number
from abjad.tools.pitchtools.diatonic_pitch_class_number_to_chromatic_pitch_class_number import diatonic_pitch_class_number_to_chromatic_pitch_class_number
from abjad.tools.pitchtools.is_chromatic_pitch_name import chromatic_pitch_name_regex
from abjad.tools.pitchtools.octave_tick_string_to_octave_number import octave_tick_string_to_octave_number


def chromatic_pitch_name_to_chromatic_pitch_number(chromatic_pitch_name):
    '''.. versionadded:: 2.0

    Change `chromatic_pitch_name` to chromatic pitch number::

        abjad> pitchtools.chromatic_pitch_name_to_chromatic_pitch_number("cs''")
        13

    Return integer or float.
    '''

    match = chromatic_pitch_name_regex.match(chromatic_pitch_name)
    if match is None:
        raise ValueError('\n\tNot chromatic pitch name: "%s".' % chromatic_pitch_name)

    groups = match.groups()
    diatonic_pitch_class_name, alphabetic_accidental_abbreviation, octave_tick_string = groups
    diatonic_pitch_class_number = diatonic_pitch_class_name_to_diatonic_pitch_class_number(
        diatonic_pitch_class_name)
    chromatic_pitch_class_number = diatonic_pitch_class_number_to_chromatic_pitch_class_number(
        diatonic_pitch_class_number)
    accidental = Accidental(alphabetic_accidental_abbreviation)
    octave_number = octave_tick_string_to_octave_number(octave_tick_string)
    chromatic_pitch_number = 12 * (octave_number - 4)
    chromatic_pitch_number += chromatic_pitch_class_number + accidental.semitones

    return chromatic_pitch_number
