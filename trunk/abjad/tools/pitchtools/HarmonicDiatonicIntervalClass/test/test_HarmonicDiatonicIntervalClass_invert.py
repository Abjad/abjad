from abjad import *


def test_HarmonicDiatonicIntervalClass_invert_01():

    hdic = pitchtools.HarmonicDiatonicIntervalClass('major', 2)
    inversion = pitchtools.HarmonicDiatonicIntervalClass('minor', 7)
    assert hdic.invert() == inversion

    hdic = pitchtools.HarmonicDiatonicIntervalClass('minor', 2)
    inversion = pitchtools.HarmonicDiatonicIntervalClass('major', 7)
    assert hdic.invert() == inversion


def test_HarmonicDiatonicIntervalClass_invert_02():

    hdic = pitchtools.HarmonicDiatonicIntervalClass('perfect', 4)
    inversion = pitchtools.HarmonicDiatonicIntervalClass('perfect', 5)
    assert hdic.invert() == inversion
