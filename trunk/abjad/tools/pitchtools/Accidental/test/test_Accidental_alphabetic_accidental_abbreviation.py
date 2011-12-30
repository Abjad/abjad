from abjad import *


def test_Accidental_alphabetic_accidental_abbreviation_01():
    t = pitchtools.Accidental('s')
    assert t.alphabetic_accidental_abbreviation == 's'


def test_Accidental_alphabetic_accidental_abbreviation_02():
    t = pitchtools.Accidental('')
    assert t.alphabetic_accidental_abbreviation == ''


def test_Accidental_alphabetic_accidental_abbreviation_03():
    t = pitchtools.Accidental()
    assert t.alphabetic_accidental_abbreviation == ''


def test_Accidental_alphabetic_accidental_abbreviation_04():
    t = pitchtools.Accidental('!')
    assert t.alphabetic_accidental_abbreviation == '!'
