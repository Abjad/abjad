from abjad import *


def testMelodicObjectChromaticInterval___add___01():

    i = pitchtools.MelodicChromaticInterval(3)
    j = pitchtools.MelodicChromaticInterval(14)

    assert i + j == pitchtools.MelodicChromaticInterval(17)
    assert j + i == pitchtools.MelodicChromaticInterval(17)


def testMelodicObjectChromaticInterval___add___02():

    i = pitchtools.MelodicChromaticInterval(3)
    j = pitchtools.MelodicChromaticInterval(14)

    assert i - j == pitchtools.MelodicChromaticInterval(-11)
    assert j - i == pitchtools.MelodicChromaticInterval(11)
