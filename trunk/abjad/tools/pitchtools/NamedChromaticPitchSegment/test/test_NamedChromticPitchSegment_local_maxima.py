from abjad import *


def test_NamedChromticPitchSegment_local_maxima_01():

    pitch_segment = pitchtools.NamedChromaticPitchSegment([-2, -1.5, 6, 7, -1.5, 7])
    assert pitch_segment.local_maxima == (pitchtools.NamedChromaticPitch(7), )
