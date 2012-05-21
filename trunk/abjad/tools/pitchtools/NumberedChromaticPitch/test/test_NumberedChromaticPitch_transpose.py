from abjad import *


def testNumberedObjectChromaticPitch_transpose_01():

    assert pitchtools.NumberedChromaticPitch(12).transpose(6) == 18
    assert pitchtools.NumberedChromaticPitch(12).transpose(-6) == 6
    assert pitchtools.NumberedChromaticPitch(12).transpose(0) == 12
    assert pitchtools.NumberedChromaticPitch(12).transpose(0.5) == 12.5
