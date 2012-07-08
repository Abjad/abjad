from abjad import *


def test_pitchtools_chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple_01():

    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(12, 'mixed')
    assert t == ('c', Accidental(''), 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(13, 'mixed')
    assert t == ('c', Accidental('s'), 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(14, 'mixed')
    assert t == ('d', Accidental(''), 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(15, 'mixed')
    assert t == ('e', Accidental('f'), 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(16, 'mixed')
    assert t == ('e', Accidental(''), 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(17, 'mixed')
    assert t == ('f', Accidental(''), 5)


def test_pitchtools_chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple_02():

    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(12, 'sharps')
    assert t == ('c', Accidental(''), 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(13, 'sharps')
    assert t == ('c', Accidental('s'), 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(14, 'sharps')
    assert t == ('d', Accidental(''), 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(15, 'sharps')
    assert t == ('d', Accidental('s'), 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(16, 'sharps')
    assert t == ('e', Accidentla(''), 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(17, 'sharps')
    assert t == ('f', Accidental(''), 5)


def test_pitchtools_chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple_03():

    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(12, 'flats')
    assert t == ('c', Accidental(''), 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(13, 'flats')
    assert t == ('d', Accidental('f'), 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(14, 'flats')
    assert t == ('d', Accidentla(''), 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(15, 'flats')
    assert t == ('e', Accidental('f'), 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(16, 'flats')
    assert t == ('e', Accidental(''), 5)
    t = pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_accidental_octave_number_triple(17, 'flats')
    assert t == ('f', Accidental(''), 5)
