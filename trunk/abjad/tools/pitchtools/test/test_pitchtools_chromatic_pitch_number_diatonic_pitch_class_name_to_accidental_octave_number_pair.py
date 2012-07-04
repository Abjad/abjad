from abjad import *


def test_pitchtools_chromatic_pitch_number_diatonic_pitch_class_name_to_accidental_octave_number_pair_01():

    t = pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_accidental_octave_number_pair(12, 'b')
    assert t == (pitchtools.Accidental('s'), 4)
    t = pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_accidental_octave_number_pair(12, 'c')
    assert t == (pitchtools.Accidental(''), 5)
    t = pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_accidental_octave_number_pair(12, 'd')
    assert t == (pitchtools.Accidental('ff'), 5)


def test_pitchtools_chromatic_pitch_number_diatonic_pitch_class_name_to_accidental_octave_number_pair_02():

    t = pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_accidental_octave_number_pair(13, 'b')
    assert t == (pitchtools.Accidental('ss'), 4)
    t = pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_accidental_octave_number_pair(13, 'c')
    assert t == (pitchtools.Accidental('s'), 5)
    t = pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_accidental_octave_number_pair(13, 'd')
    assert t == (pitchtools.Accidental('f'), 5)


def test_pitchtools_chromatic_pitch_number_diatonic_pitch_class_name_to_accidental_octave_number_pair_03():

    t = pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_accidental_octave_number_pair(14, 'c')
    assert t == (pitchtools.Accidental('ss'), 5)
    t = pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_accidental_octave_number_pair(14, 'd')
    assert t == (pitchtools.Accidental(''), 5)
    t = pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_accidental_octave_number_pair(14, 'e')
    assert t == (pitchtools.Accidental('ff'), 5)
