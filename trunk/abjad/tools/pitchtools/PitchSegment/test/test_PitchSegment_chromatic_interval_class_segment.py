from abjad import *


def test_PitchSegment_chromatic_interval_class_segment_01( ):

   pitch_segment = pitchtools.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
   interval_class_segment = pitch_segment.chromatic_interval_class_segment
   assert interval_class_segment == [0.5, 7.5, 1, -8.5, 8.5]
