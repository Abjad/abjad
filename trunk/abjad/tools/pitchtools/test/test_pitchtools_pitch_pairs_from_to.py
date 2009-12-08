from abjad import *


def test_pitchtools_pitch_pairs_from_to_01( ):

   chord_1 = Chord([0, 1, 2], (1, 4))
   chord_2 = Chord([3, 4], (1, 4))
   pairs = pitchtools.pitch_pairs_from_to(chord_1, chord_2)
   pairs = list(pairs)

   assert pairs[0] == (Pitch(0), Pitch(3))
   assert pairs[1] == (Pitch(0), Pitch(4))
   assert pairs[2] == (Pitch(1), Pitch(3))
   assert pairs[3] == (Pitch(1), Pitch(4))
   assert pairs[4] == (Pitch(2), Pitch(3))
   assert pairs[5] == (Pitch(2), Pitch(4))
