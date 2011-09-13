from abjad import *


def test_NamedChromticPitchSegment_melodic_diatonic_interval_segment_01():

    pitch_segment = pitchtools.NamedChromaticPitchSegment([-2, -1, 6, 7, -1, 7])

    assert pitch_segment.melodic_diatonic_interval_segment == \
        pitchtools.MelodicDiatonicIntervalSegment([
        pitchtools.MelodicDiatonicInterval('augmented', 1),
        pitchtools.MelodicDiatonicInterval('perfect', 5),
        pitchtools.MelodicDiatonicInterval('minor', 2),
        pitchtools.MelodicDiatonicInterval('minor', -6),
        pitchtools.MelodicDiatonicInterval('minor', 6)])
