from abjad import *


def test_pitchtools_list_ordered_pitch_pairs_from_expr_cross_to_expr_01( ):

   chord_1 = Chord([0, 1, 2], (1, 4))
   chord_2 = Chord([3, 4], (1, 4))
   pairs = pitchtools.list_ordered_pitch_pairs_from_expr_cross_to_expr(chord_1, chord_2)
   pairs = list(pairs)

   assert pairs[0] == (pitchtools.NamedPitch(0), pitchtools.NamedPitch(3))
   assert pairs[1] == (pitchtools.NamedPitch(0), pitchtools.NamedPitch(4))
   assert pairs[2] == (pitchtools.NamedPitch(1), pitchtools.NamedPitch(3))
   assert pairs[3] == (pitchtools.NamedPitch(1), pitchtools.NamedPitch(4))
   assert pairs[4] == (pitchtools.NamedPitch(2), pitchtools.NamedPitch(3))
   assert pairs[5] == (pitchtools.NamedPitch(2), pitchtools.NamedPitch(4))
