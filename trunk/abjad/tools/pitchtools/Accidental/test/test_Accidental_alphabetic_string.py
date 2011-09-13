from abjad import *


def test_Accidental_alphabetic_string_01():
    t = pitchtools.Accidental('s')
    assert t.alphabetic_string == 's'


def test_Accidental_alphabetic_string_02():
    t = pitchtools.Accidental('')
    assert t.alphabetic_string == ''


def test_Accidental_alphabetic_string_03():
    t = pitchtools.Accidental()
    assert t.alphabetic_string == ''


def test_Accidental_alphabetic_string_04():
    t = pitchtools.Accidental('!')
    assert t.alphabetic_string == '!'
