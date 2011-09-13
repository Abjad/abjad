from abjad import *


def test_NamedChromaticPitchVector___init___01():

    ncpv = pitchtools.NamedChromaticPitchVector(["c''", "c''", "cs''", "cs''", "cs''"])

    assert sorted(ncpv.items()) == [("c''", 2), ("cs''", 3)]
