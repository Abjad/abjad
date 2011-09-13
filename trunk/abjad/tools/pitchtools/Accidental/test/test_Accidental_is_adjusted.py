from abjad import *


def test_Accidental_is_adjusted_01():

    assert pitchtools.Accidental('sharp').is_adjusted
    assert pitchtools.Accidental('flat').is_adjusted


def test_Accidental_is_adjusted_02():

    assert not pitchtools.Accidental('natural').is_adjusted
    assert not pitchtools.Accidental('!').is_adjusted
    assert not pitchtools.Accidental('').is_adjusted
