from abjad import *
from abjad.tools import tonalitytools


def test_Mode_melodic_diatonic_interval_segment_01():

    m2 = pitchtools.MelodicDiatonicInterval('minor', 2)
    M2 = pitchtools.MelodicDiatonicInterval('major', 2)

    mdig = tonalitytools.Mode('dorian').melodic_diatonic_interval_segment
    intervals = [M2, m2, M2, M2, M2, m2, M2]
    assert mdig == pitchtools.MelodicDiatonicIntervalSegment(intervals)

    mdig = tonalitytools.Mode('phrygian').melodic_diatonic_interval_segment
    intervals = [m2, M2, M2, M2, m2, M2, M2]
    assert mdig == pitchtools.MelodicDiatonicIntervalSegment(intervals)

    mdig = tonalitytools.Mode('lydian').melodic_diatonic_interval_segment
    intervals = [M2, M2, M2, m2, M2, M2, m2]
    assert mdig == pitchtools.MelodicDiatonicIntervalSegment(intervals)
