from abjad import *


def test_HarmonicChromaticIntervalClassVector_has_none_of_01():

    civ = pitchtools.HarmonicChromaticIntervalClassVector(Staff("c'8 d'8 e'8 f'8 g'8"))

    "0 1 3 2 1 2 0 1 0 0 0 0"

    assert not civ.has_none_of([0, 1, 2])
    assert not civ.has_none_of([3, 4, 5])
    assert not civ.has_none_of([6, 7, 8])
    assert civ.has_none_of([9, 10, 11])
