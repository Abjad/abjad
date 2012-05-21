from abjad import *


def testNumberedObjectChromaticPitch___float___01():
    '''Return chromatic pitch number of 12-ET numbered chromatic pitch as float.
    '''

    numbered_chromatic_pitch = pitchtools.NumberedChromaticPitch(13)
    assert isinstance(float(numbered_chromatic_pitch), float)
    assert float(numbered_chromatic_pitch) == 13.0


def testNumberedObjectChromaticPitch___float___02():
    '''Return chromatic pitch number of 24-ET numbered chromatic pitch as float.
    '''

    numbered_chromatic_pitch = pitchtools.NumberedChromaticPitch(13.5)
    assert isinstance(float(numbered_chromatic_pitch), float)
    assert float(numbered_chromatic_pitch) == 13.5
