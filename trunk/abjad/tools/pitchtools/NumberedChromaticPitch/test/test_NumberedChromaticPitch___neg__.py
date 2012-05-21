from abjad import *


def testNumberedObjectChromaticPitch___neg___01():

    assert -pitchtools.NumberedChromaticPitch(12) == -12
