from abjad import *


def test_PitchSegment_local_minima_01( ):

   pitch_segment = pitchtools.NamedPitchSegment([-2, -1.5, 6, 7, -1.5, 7])
   assert pitch_segment.local_minima == (pitchtools.NamedPitch(-1.5), )
