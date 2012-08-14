from abjad import *


def test_pitchtools_spell_chromatic_pitch_number_01():

    t = pitchtools.spell_chromatic_pitch_number(12, 'b')
    assert t == (pitchtools.Accidental('s'), 4)
    t = pitchtools.spell_chromatic_pitch_number(12, 'c')
    assert t == (pitchtools.Accidental(''), 5)
    t = pitchtools.spell_chromatic_pitch_number(12, 'd')
    assert t == (pitchtools.Accidental('ff'), 5)


def test_pitchtools_spell_chromatic_pitch_number_02():

    t = pitchtools.spell_chromatic_pitch_number(13, 'b')
    assert t == (pitchtools.Accidental('ss'), 4)
    t = pitchtools.spell_chromatic_pitch_number(13, 'c')
    assert t == (pitchtools.Accidental('s'), 5)
    t = pitchtools.spell_chromatic_pitch_number(13, 'd')
    assert t == (pitchtools.Accidental('f'), 5)


def test_pitchtools_spell_chromatic_pitch_number_03():

    t = pitchtools.spell_chromatic_pitch_number(14, 'c')
    assert t == (pitchtools.Accidental('ss'), 5)
    t = pitchtools.spell_chromatic_pitch_number(14, 'd')
    assert t == (pitchtools.Accidental(''), 5)
    t = pitchtools.spell_chromatic_pitch_number(14, 'e')
    assert t == (pitchtools.Accidental('ff'), 5)
