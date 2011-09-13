from abjad import *


def test_NamedChromticPitchSegment_melodic_chromatic_interval_class_segment_01():

    pitch_segment = pitchtools.NamedChromaticPitchSegment([-2, -1.5, 6, 7, -1.5, 7])
    result = pitch_segment.melodic_chromatic_interval_class_segment
    #assert result == [0.5, 7.5, 1, -8.5, 8.5]
    assert result == [
        pitchtools.MelodicChromaticIntervalClass(0.5),
        pitchtools.MelodicChromaticIntervalClass(7.5),
        pitchtools.MelodicChromaticIntervalClass(1),
        pitchtools.MelodicChromaticIntervalClass(-8.5),
        pitchtools.MelodicChromaticIntervalClass(8.5)]
