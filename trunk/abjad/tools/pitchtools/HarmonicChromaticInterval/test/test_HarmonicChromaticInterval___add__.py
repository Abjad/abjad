from abjad import *


def test_HarmonicChromaticInterval___add___01():

    i = pitchtools.HarmonicChromaticInterval(3)
    j = pitchtools.HarmonicChromaticInterval(14)

    assert i + j == pitchtools.HarmonicChromaticInterval(17)
    assert j + i == pitchtools.HarmonicChromaticInterval(17)


def test_HarmonicChromaticInterval___add___02():

    i = pitchtools.HarmonicChromaticInterval(3)
    j = pitchtools.HarmonicChromaticInterval(14)

    assert i - j == pitchtools.HarmonicChromaticInterval(11)
    assert j - i == pitchtools.HarmonicChromaticInterval(11)
