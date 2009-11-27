from abjad import *


def test_PitchSegment___max___01( ):

   pitch_segment = pitchtools.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
   assert max(pitch_segment) == Pitch(7)
