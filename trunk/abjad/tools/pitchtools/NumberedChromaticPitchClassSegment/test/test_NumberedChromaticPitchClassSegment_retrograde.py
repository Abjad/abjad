from abjad import *


def test_NumberedChromaticPitchClassSegment_retrograde_01():

    pcseg = pitchtools.NumberedChromaticPitchClassSegment([0, 6, 10, 4, 9, 2])
    PCSeg = pitchtools.NumberedChromaticPitchClassSegment

    assert pcseg.retrograde() == PCSeg([2, 9, 4, 10, 6, 0])
