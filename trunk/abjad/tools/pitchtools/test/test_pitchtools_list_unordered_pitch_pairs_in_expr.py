from abjad import *


def test_pitchtools_list_unordered_pitch_pairs_in_expr_01( ):

   chord = Chord([0, 1, 2, 3], (1, 4))
   pairs = pitchtools.list_unordered_pitch_pairs_in_expr(chord)
   pairs = list(pairs)

   assert pairs[0] == (pitchtools.NamedPitch(0), pitchtools.NamedPitch(1))
   assert pairs[1] == (pitchtools.NamedPitch(0), pitchtools.NamedPitch(2))
   assert pairs[2] == (pitchtools.NamedPitch(0), pitchtools.NamedPitch(3))
   assert pairs[3] == (pitchtools.NamedPitch(1), pitchtools.NamedPitch(2))
   assert pairs[4] == (pitchtools.NamedPitch(1), pitchtools.NamedPitch(3))
   assert pairs[5] == (pitchtools.NamedPitch(2), pitchtools.NamedPitch(3))
