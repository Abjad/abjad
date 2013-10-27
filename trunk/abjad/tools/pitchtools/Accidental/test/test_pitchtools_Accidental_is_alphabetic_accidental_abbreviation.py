# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_Accidental_is_alphabetic_accidental_abbreviation_01():

    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('s')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('ss')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('f')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('ff')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('qs')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('tqs')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('qf')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('tqf')


def test_pitchtools_Accidental_is_alphabetic_accidental_abbreviation_02():

    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('!')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('s!')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('ss!')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('f!')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('ff!')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('qs!')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('tqs!')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('qf!')
    assert pitchtools.Accidental.is_alphabetic_accidental_abbreviation('tqf!')


def test_pitchtools_Accidental_is_alphabetic_accidental_abbreviation_03():

    assert not pitchtools.Accidental.is_alphabetic_accidental_abbreviation(8)
