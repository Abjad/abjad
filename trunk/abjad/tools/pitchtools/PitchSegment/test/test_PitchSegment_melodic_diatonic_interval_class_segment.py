from abjad import *


def test_PitchSegment_melodic_diatonic_interval_class_segment_01( ):

   pitch_segment = pitchtools.PitchSegment([-2, -1, 6, 7, -1, 7])

   assert pitch_segment.melodic_diatonic_interval_class_segment == [
      1, 5, 2, -6, 6]
