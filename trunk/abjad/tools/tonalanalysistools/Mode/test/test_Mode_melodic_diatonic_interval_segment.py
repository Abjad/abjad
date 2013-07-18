from abjad import *
from abjad.tools import tonalanalysistools


def test_Mode_melodic_diatonic_interval_segment_01():

    m2 = pitchtools.MelodicDiatonicInterval('minor', 2)
    M2 = pitchtools.MelodicDiatonicInterval('major', 2)

    mdig = tonalanalysistools.Mode('dorian').melodic_diatonic_interval_segment
    intervals = [M2, m2, M2, M2, M2, m2, M2]
    assert mdig == pitchtools.MelodicDiatonicIntervalSegment(intervals)

    mdig = tonalanalysistools.Mode('phrygian').melodic_diatonic_interval_segment
    intervals = [m2, M2, M2, M2, m2, M2, M2]
    assert mdig == pitchtools.MelodicDiatonicIntervalSegment(intervals)

    mdig = tonalanalysistools.Mode('lydian').melodic_diatonic_interval_segment
    intervals = [M2, M2, M2, m2, M2, M2, m2]
    assert mdig == pitchtools.MelodicDiatonicIntervalSegment(intervals)
