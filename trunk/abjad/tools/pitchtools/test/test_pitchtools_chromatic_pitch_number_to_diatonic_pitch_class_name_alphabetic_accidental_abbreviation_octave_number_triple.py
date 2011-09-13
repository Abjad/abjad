from abjad import *


def test_pitchtools_chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple_01():

    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(12, 'mixed')
    assert t == ('c', '', 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(13, 'mixed')
    assert t == ('c', 's', 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(14, 'mixed')
    assert t == ('d', '', 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(15, 'mixed')
    assert t == ('e', 'f', 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(16, 'mixed')
    assert t == ('e', '', 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(17, 'mixed')
    assert t == ('f', '', 5)


def test_pitchtools_chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple_02():

    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(12, 'sharps')
    assert t == ('c', '', 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(13, 'sharps')
    assert t == ('c', 's', 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(14, 'sharps')
    assert t == ('d', '', 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(15, 'sharps')
    assert t == ('d', 's', 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(16, 'sharps')
    assert t == ('e', '', 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(17, 'sharps')
    assert t == ('f', '', 5)


def test_pitchtools_chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple_03():

    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(12, 'flats')
    assert t == ('c', '', 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(13, 'flats')
    assert t == ('d', 'f', 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(14, 'flats')
    assert t == ('d', '', 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(15, 'flats')
    assert t == ('e', 'f', 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(16, 'flats')
    assert t == ('e', '', 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_abbreviation_octave_number_triple(17, 'flats')
    assert t == ('f', '', 5)
