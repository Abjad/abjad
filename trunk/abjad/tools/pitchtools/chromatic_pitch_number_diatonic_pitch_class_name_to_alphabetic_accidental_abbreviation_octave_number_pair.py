from abjad.tools.pitchtools.Accidental import Accidental
from abjad.tools.pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number import chromatic_pitch_number_and_accidental_semitones_to_octave_number
from abjad.tools.pitchtools.diatonic_pitch_class_name_to_chromatic_pitch_class_number import diatonic_pitch_class_name_to_chromatic_pitch_class_number
from abjad.tools.pitchtools.transpose_chromatic_pitch_class_number_by_octaves_to_nearest_neighbor_of_chromatic_pitch_number import transpose_chromatic_pitch_class_number_by_octaves_to_nearest_neighbor_of_chromatic_pitch_number


def chromatic_pitch_number_diatonic_pitch_class_name_to_alphabetic_accidental_abbreviation_octave_number_pair(chromatic_pitch_number, diatonic_pitch_class_name):
    '''.. versionadded:: 1.1

    Change `chromatic_pitch_number` and `diatonic_pitch_class_name` to
    alphabetic accidental abbreviation / octave number pair::

        abjad> pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_alphabetic_accidental_abbreviation_octave_number_pair(14, 'c')
        ('ss', 5)

    Return pair.

    .. versionchanged:: 2.0
        renamed ``pitchtools.number_letter_to_accidental_octave()`` to
        ``pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_alphabetic_accidental_abbreviation_octave_number_pair()``.
    '''

    # check input
    if not isinstance(chromatic_pitch_number, (int, long, float)):
        raise TypeError

    if not isinstance(diatonic_pitch_class_name, str):
        raise TypeError

    if not diatonic_pitch_class_name in ['c', 'd', 'e', 'f', 'g', 'a', 'b']:
        raise ValueError

    # find accidental semitones
    pc = diatonic_pitch_class_name_to_chromatic_pitch_class_number(diatonic_pitch_class_name)
    nearest_neighbor = transpose_chromatic_pitch_class_number_by_octaves_to_nearest_neighbor_of_chromatic_pitch_number(chromatic_pitch_number, pc)
    semitones = chromatic_pitch_number - nearest_neighbor

    # find accidental alphabetic string
    alphabetic_accidental_abbreviation = Accidental._semitones_to_alphabetic_accidental_abbreviation[semitones]

    # find octave
    octave = chromatic_pitch_number_and_accidental_semitones_to_octave_number(
        chromatic_pitch_number, semitones)

    # return unique pair of accidental string and octave
    return alphabetic_accidental_abbreviation, octave
