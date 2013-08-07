# -*- encoding: utf-8 -*-
from abjad import *


def test_Accidental_alphabetic_accidental_abbreviation_01():
    accidental = pitchtools.Accidental('s')
    assert accidental.alphabetic_accidental_abbreviation == 's'


def test_Accidental_alphabetic_accidental_abbreviation_02():
    accidental = pitchtools.Accidental('')
    assert accidental.alphabetic_accidental_abbreviation == ''


def test_Accidental_alphabetic_accidental_abbreviation_03():
    accidental = pitchtools.Accidental()
    assert accidental.alphabetic_accidental_abbreviation == ''


def test_Accidental_alphabetic_accidental_abbreviation_04():
    t = pitchtools.Accidental('!')
    assert t.alphabetic_accidental_abbreviation == '!'
