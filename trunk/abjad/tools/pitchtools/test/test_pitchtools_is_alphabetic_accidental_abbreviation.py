from abjad import *


def test_pitchtools_is_alphabetic_accidental_abbreviation_01():

    assert pitchtools.is_alphabetic_accidental_abbreviation('')
    assert pitchtools.is_alphabetic_accidental_abbreviation('s')
    assert pitchtools.is_alphabetic_accidental_abbreviation('ss')
    assert pitchtools.is_alphabetic_accidental_abbreviation('f')
    assert pitchtools.is_alphabetic_accidental_abbreviation('ff')
    assert pitchtools.is_alphabetic_accidental_abbreviation('qs')
    assert pitchtools.is_alphabetic_accidental_abbreviation('tqs')
    assert pitchtools.is_alphabetic_accidental_abbreviation('qf')
    assert pitchtools.is_alphabetic_accidental_abbreviation('tqf')


def test_pitchtools_is_alphabetic_accidental_abbreviation_02():

    assert pitchtools.is_alphabetic_accidental_abbreviation('!')
    assert pitchtools.is_alphabetic_accidental_abbreviation('s!')
    assert pitchtools.is_alphabetic_accidental_abbreviation('ss!')
    assert pitchtools.is_alphabetic_accidental_abbreviation('f!')
    assert pitchtools.is_alphabetic_accidental_abbreviation('ff!')
    assert pitchtools.is_alphabetic_accidental_abbreviation('qs!')
    assert pitchtools.is_alphabetic_accidental_abbreviation('tqs!')
    assert pitchtools.is_alphabetic_accidental_abbreviation('qf!')
    assert pitchtools.is_alphabetic_accidental_abbreviation('tqf!')


def test_pitchtools_is_alphabetic_accidental_abbreviation_03():

    assert not pitchtools.is_alphabetic_accidental_abbreviation(8)
