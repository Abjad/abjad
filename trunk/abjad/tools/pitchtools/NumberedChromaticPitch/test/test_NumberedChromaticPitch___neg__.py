from abjad import *


def test_NumberedChromaticPitch___neg___01():

    assert -pitchtools.NumberedChromaticPitch(12) == -12
