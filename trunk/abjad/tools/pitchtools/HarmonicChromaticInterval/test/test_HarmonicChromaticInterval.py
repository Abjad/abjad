from abjad import *
import py.test


def test_HarmonicChromaticInterval_01():

    i = pitchtools.HarmonicChromaticInterval(3)

    assert abs(i) == pitchtools.HarmonicChromaticInterval(3)
    assert int(i) == 3
    assert float(i) == 3.0

    assert py.test.raises(TypeError, '-i')
