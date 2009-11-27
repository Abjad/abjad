from abjad import *


def test_PitchSegment_diatonic_interval_segment_01( ):

   pitch_segment = pitchtools.PitchSegment([-2, -1, 6, 7, -1, 7])
   assert pitch_segment.diatonic_interval_segment == [
      pitchtools.DiatonicInterval('augmented', -1),
      pitchtools.DiatonicInterval('perfect', -5),
      pitchtools.DiatonicInterval('minor', -2),
      pitchtools.DiatonicInterval('minor', 6),
      pitchtools.DiatonicInterval('minor', -6)]
