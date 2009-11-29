from abjad import *


def test_PitchSegment_melodic_chromatic_interval_class_segment_01( ):

   pitch_segment = pitchtools.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
   result = pitch_segment.melodic_chromatic_interval_class_segment
   assert result == [0.5, 7.5, 1, -8.5, 8.5]
