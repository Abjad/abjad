from abjad import *


def testNumberedObjectChromaticPitchClassSegment___mul___01():

    ncpcs1 = pitchtools.NumberedChromaticPitchClassSegment([0, 1, 11, 9])
    ncpsc2 = ncpcs1 * 2

    assert ncpsc2 == pitchtools.NumberedChromaticPitchClassSegment([0, 1, 11, 9, 0, 1, 11, 9])
