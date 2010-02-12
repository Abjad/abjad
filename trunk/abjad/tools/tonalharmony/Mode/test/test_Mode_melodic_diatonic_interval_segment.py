from abjad import *


def test_Mode_melodic_diatonic_interval_segment_01( ):

   m2 = pitchtools.MelodicDiatonicInterval('minor', 2)
   M2 = pitchtools.MelodicDiatonicInterval('major', 2)

   mdig = tonalharmony.Mode('dorian').melodic_diatonic_interval_segment
   intervals = [M2, m2, M2, M2, M2, m2, M2]
   assert mdig == pitchtools.MelodicDiatonicIntervalSegment(intervals)

   mdig = tonalharmony.Mode('phrygian').melodic_diatonic_interval_segment
   intervals = [m2, M2, M2, M2, m2, M2, M2]
   assert mdig == pitchtools.MelodicDiatonicIntervalSegment(intervals)

   mdig = tonalharmony.Mode('lydian').melodic_diatonic_interval_segment
   intervals = [M2, M2, M2, m2, M2, M2, m2]
   assert mdig == pitchtools.MelodicDiatonicIntervalSegment(intervals)

