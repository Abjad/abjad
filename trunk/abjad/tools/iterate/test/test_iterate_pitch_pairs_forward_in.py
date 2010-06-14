from abjad import *


def test_iterate_pitch_pairs_forward_in_01( ):

   score = Score([ ])
   notes = leaftools.make_first_n_notes_in_ascending_diatonic_scale(4) + [Note(7, (1, 4))]
   score.append(Staff(notes))
   notes = [Note(x, (1, 4)) for x in [-12, -15, -17]]
   score.append(Staff(notes))
   score[1].clef.forced = Clef('bass')

   r'''
   \new Score <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
                   g'4
           }
           \new Staff {
                   \clef "bass"
                   c4
                   a,4
                   g,4
           }
   >>
   '''

   pairs = iterate.pitch_pairs_forward_in(score)
   pairs = list(pairs)

   assert pairs[0] == (Pitch('c', 4), Pitch('c', 3)) #
   assert pairs[1] == (Pitch('c', 4), Pitch('d', 4))
   assert pairs[2] == (Pitch('c', 3), Pitch('d', 4))
   assert pairs[3] == (Pitch('d', 4), Pitch('e', 4))
   assert pairs[4] == (Pitch('d', 4), Pitch('a', 2))
   assert pairs[5] == (Pitch('c', 3), Pitch('e', 4))
   assert pairs[6] == (Pitch('c', 3), Pitch('a', 2))
   assert pairs[7] == (Pitch('e', 4), Pitch('a', 2))
   assert pairs[8] == (Pitch('e', 4), Pitch('f', 4))
   assert pairs[9] == (Pitch('a', 2), Pitch('f', 4))
   assert pairs[10] == (Pitch('f', 4), Pitch('g', 4))
   assert pairs[11] == (Pitch('f', 4), Pitch('g', 2))
   assert pairs[12] == (Pitch('a', 2), Pitch('g', 4))
   assert pairs[13] == (Pitch('a', 2), Pitch('g', 2))
   assert pairs[14] == (Pitch('g', 4), Pitch('g', 2))


def test_iterate_pitch_pairs_forward_in_02( ):

   chord_1 = Chord([0, 2, 4], (1, 4))
   chord_2 = Chord([17, 19], (1, 4))
   staff = Staff([chord_1, chord_2])

   r'''
   \new Staff {
           <c' d' e'>4
           <f'' g''>4
   }
   '''

   pairs = iterate.pitch_pairs_forward_in(staff)
   pairs = list(pairs)

   assert pairs[0] == (Pitch('c', 4), Pitch('d', 4))
   assert pairs[1] == (Pitch('c', 4), Pitch('e', 4))
   assert pairs[2] == (Pitch('d', 4), Pitch('e', 4))
   assert pairs[3] == (Pitch('c', 4), Pitch('f', 5))
   assert pairs[4] == (Pitch('c', 4), Pitch('g', 5))
   assert pairs[5] == (Pitch('d', 4), Pitch('f', 5))
   assert pairs[6] == (Pitch('d', 4), Pitch('g', 5))
   assert pairs[7] == (Pitch('e', 4), Pitch('f', 5))
   assert pairs[8] == (Pitch('e', 4), Pitch('g', 5))
   assert pairs[9] == (Pitch('f', 5), Pitch('g', 5))
