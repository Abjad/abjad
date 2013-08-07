# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_chromatic_pitch_number_to_chromatic_pitch_triple_01():

    accidental = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(12, 'mixed')
    assert accidental == ('c', pitchtools.Accidental(''), 5)
    accidental = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(13, 'mixed')
    assert accidental == ('c', pitchtools.Accidental('s'), 5)
    accidental = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(14, 'mixed')
    assert accidental == ('d', pitchtools.Accidental(''), 5)
    accidental = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(15, 'mixed')
    assert accidental == ('e', pitchtools.Accidental('f'), 5)
    accidental = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(16, 'mixed')
    assert accidental == ('e', pitchtools.Accidental(''), 5)
    accidental = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(17, 'mixed')
    assert accidental == ('f', pitchtools.Accidental(''), 5)


def test_pitchtools_chromatic_pitch_number_to_chromatic_pitch_triple_02():

    accidental = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(12, 'sharps')
    assert accidental == ('c', pitchtools.Accidental(''), 5)
    accidental = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(13, 'sharps')
    assert accidental == ('c', pitchtools.Accidental('s'), 5)
    accidental = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(14, 'sharps')
    assert accidental == ('d', pitchtools.Accidental(''), 5)
    accidental = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(15, 'sharps')
    assert accidental == ('d', pitchtools.Accidental('s'), 5)
    accidental = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(16, 'sharps')
    assert accidental == ('e', pitchtools.Accidental(''), 5)
    accidental = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(17, 'sharps')
    assert accidental == ('f', pitchtools.Accidental(''), 5)


def test_pitchtools_chromatic_pitch_number_to_chromatic_pitch_triple_03():

    t = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(12, 'flats')
    assert t == ('c', pitchtools.Accidental(''), 5)
    t = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(13, 'flats')
    assert t == ('d', pitchtools.Accidental('f'), 5)
    t = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(14, 'flats')
    assert t == ('d', pitchtools.Accidental(''), 5)
    t = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(15, 'flats')
    assert t == ('e', pitchtools.Accidental('f'), 5)
    t = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(16, 'flats')
    assert t == ('e', pitchtools.Accidental(''), 5)
    t = pitchtools.chromatic_pitch_number_to_chromatic_pitch_triple(17, 'flats')
    assert t == ('f', pitchtools.Accidental(''), 5)
