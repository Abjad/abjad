from abjad import *


def test_NamedChromticPitchSegment_melodic_diatonic_interval_class_segment_01():

    pitch_segment = pitchtools.NamedChromaticPitchSegment([-2, -1, 6, 7, -1, 7])

    #assert pitch_segment.melodic_diatonic_interval_class_segment == [
    #    1, 5, 2, -6, 6]

    assert pitch_segment.melodic_diatonic_interval_class_segment == [
        pitchtools.MelodicDiatonicIntervalClass('augmented', 1),
        pitchtools.MelodicDiatonicIntervalClass('perfect', 5),
        pitchtools.MelodicDiatonicIntervalClass('minor', 2),
        pitchtools.MelodicDiatonicIntervalClass('minor', -6),
        pitchtools.MelodicDiatonicIntervalClass('minor', 6)]
