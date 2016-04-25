# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Accidental_is_abbreviation_01():

    assert pitchtools.Accidental.is_abbreviation('')
    assert pitchtools.Accidental.is_abbreviation('s')
    assert pitchtools.Accidental.is_abbreviation('ss')
    assert pitchtools.Accidental.is_abbreviation('f')
    assert pitchtools.Accidental.is_abbreviation('ff')
    assert pitchtools.Accidental.is_abbreviation('qs')
    assert pitchtools.Accidental.is_abbreviation('tqs')
    assert pitchtools.Accidental.is_abbreviation('qf')
    assert pitchtools.Accidental.is_abbreviation('tqf')


def test_pitchtools_Accidental_is_abbreviation_02():

    assert pitchtools.Accidental.is_abbreviation('!')
    assert pitchtools.Accidental.is_abbreviation('s!')
    assert pitchtools.Accidental.is_abbreviation('ss!')
    assert pitchtools.Accidental.is_abbreviation('f!')
    assert pitchtools.Accidental.is_abbreviation('ff!')
    assert pitchtools.Accidental.is_abbreviation('qs!')
    assert pitchtools.Accidental.is_abbreviation('tqs!')
    assert pitchtools.Accidental.is_abbreviation('qf!')
    assert pitchtools.Accidental.is_abbreviation('tqf!')


def test_pitchtools_Accidental_is_abbreviation_03():

    assert not pitchtools.Accidental.is_abbreviation(8)
