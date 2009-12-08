from abjad import *


def test_pitchtools_pitch_pairs_within_01( ):

   chord = Chord([0, 1, 2, 3], (1, 4))
   pairs = pitchtools.pitch_pairs_within(chord)
   pairs = list(pairs)

   assert pairs[0] == set([Pitch(0), Pitch(1)])
   assert pairs[1] == set([Pitch(0), Pitch(2)])
   assert pairs[2] == set([Pitch(0), Pitch(3)])
   assert pairs[3] == set([Pitch(1), Pitch(2)])
   assert pairs[4] == set([Pitch(1), Pitch(3)])
   assert pairs[5] == set([Pitch(2), Pitch(3)])
