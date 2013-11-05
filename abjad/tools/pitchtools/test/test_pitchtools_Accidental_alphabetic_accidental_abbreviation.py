# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_Accidental_alphabetic_accidental_abbreviation_01():
    accidental = pitchtools.Accidental('s')
    assert accidental.alphabetic_accidental_abbreviation == 's'


def test_pitchtools_Accidental_alphabetic_accidental_abbreviation_02():
    accidental = pitchtools.Accidental('')
    assert accidental.alphabetic_accidental_abbreviation == ''


def test_pitchtools_Accidental_alphabetic_accidental_abbreviation_03():
    accidental = pitchtools.Accidental()
    assert accidental.alphabetic_accidental_abbreviation == ''


def test_pitchtools_Accidental_alphabetic_accidental_abbreviation_04():
    accidental = pitchtools.Accidental('!')
    assert accidental.alphabetic_accidental_abbreviation == '!'


def test_pitchtools_Accidental_alphabetic_accidental_abbreviation_05():

    assert pitchtools.Accidental('').alphabetic_accidental_abbreviation == ''
    assert pitchtools.Accidental('!').alphabetic_accidental_abbreviation == '!'
    assert pitchtools.Accidental('bb').alphabetic_accidental_abbreviation == 'ff'
    assert pitchtools.Accidental('b~').alphabetic_accidental_abbreviation == 'tqf'
    assert pitchtools.Accidental('b').alphabetic_accidental_abbreviation == 'f'
    assert pitchtools.Accidental('~').alphabetic_accidental_abbreviation == 'qf'
    assert pitchtools.Accidental('##').alphabetic_accidental_abbreviation == 'ss'
    assert pitchtools.Accidental('#+').alphabetic_accidental_abbreviation == 'tqs'
    assert pitchtools.Accidental('#').alphabetic_accidental_abbreviation == 's'
    assert pitchtools.Accidental('+').alphabetic_accidental_abbreviation == 'qs'
