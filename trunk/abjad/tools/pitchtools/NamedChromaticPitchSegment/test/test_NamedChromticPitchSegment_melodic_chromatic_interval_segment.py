from abjad import *


def test_NamedChromticPitchSegment_melodic_chromatic_interval_segment_01():

    pitch_segment = pitchtools.NamedChromaticPitchSegment([-2, -1.5, 6, 7, -1.5, 7])
    result = pitch_segment.melodic_chromatic_interval_segment
    intervals = [0.5, 7.5, 1, -8.5, 8.5]
    #assert result == [pitchtools.MelodicChromaticInterval(x) for x in intervals]
    assert result == pitchtools.MelodicChromaticIntervalSegment(intervals)
