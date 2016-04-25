# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Accidental_abbreviation_01():
    accidental = pitchtools.Accidental('s')
    assert accidental.abbreviation == 's'


def test_pitchtools_Accidental_abbreviation_02():
    accidental = pitchtools.Accidental('')
    assert accidental.abbreviation == ''


def test_pitchtools_Accidental_abbreviation_03():
    accidental = pitchtools.Accidental()
    assert accidental.abbreviation == ''


def test_pitchtools_Accidental_abbreviation_04():
    accidental = pitchtools.Accidental('!')
    assert accidental.abbreviation == '!'


def test_pitchtools_Accidental_abbreviation_05():

    assert pitchtools.Accidental('').abbreviation == ''
    assert pitchtools.Accidental('!').abbreviation == '!'
    assert pitchtools.Accidental('bb').abbreviation == 'ff'
    assert pitchtools.Accidental('b~').abbreviation == 'tqf'
    assert pitchtools.Accidental('b').abbreviation == 'f'
    assert pitchtools.Accidental('~').abbreviation == 'qf'
    assert pitchtools.Accidental('##').abbreviation == 'ss'
    assert pitchtools.Accidental('#+').abbreviation == 'tqs'
    assert pitchtools.Accidental('#').abbreviation == 's'
    assert pitchtools.Accidental('+').abbreviation == 'qs'
