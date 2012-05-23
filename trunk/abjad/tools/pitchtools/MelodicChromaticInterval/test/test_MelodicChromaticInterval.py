from abjad import *


def test_MelodicChromaticInterval_01():

    i = pitchtools.MelodicChromaticInterval(3)

    assert abs(i) == pitchtools.HarmonicChromaticInterval(3)
    assert -i == pitchtools.MelodicChromaticInterval(-3)
    assert int(i) == 3
    assert float(i) == 3.0
