from abjad import *


def test_iterate_vertical_moments_forward_in_expr_01( ):

   score = Score([ ])
   score.append(Staff([FixedDurationTuplet((4, 8), leaftools.make_repeated_notes(3))]))
   piano_staff = PianoStaff([ ])
   piano_staff.append(Staff(leaftools.make_repeated_notes(2, Rational(1, 4))))
   piano_staff.append(Staff(leaftools.make_repeated_notes(4)))
   piano_staff[1].clef.forced = Clef('bass')
   score.append(piano_staff)
   pitchtools.diatonicize(list(reversed(score.leaves)))

   r'''
   \new Score <<
           \new Staff {
                   \times 4/3 {
                           d''8
                           c''8
                           b'8
                   }
           }
           \new PianoStaff <<
                   \new Staff {
                           a'4
                           g'4
                   }
                   \new Staff {
                           \clef "bass"
                           f'8
                           e'8
                           d'8
                           c'8
                   }
           >>
   >>
   '''

   moment_generator = iterate.vertical_moments_forward_in_expr(score)
   moments = list(moment_generator)

   r'''
   (Note(d'', 8), Note(a', 4), Note(f', 8))
   (Note(d'', 8), Note(a', 4), Note(e', 8))
   (Note(c'', 8), Note(a', 4), Note(e', 8))
   (Note(c'', 8), Note(g', 4), Note(d', 8))
   (Note(b', 8), Note(g', 4), Note(d', 8))
   (Note(b', 8), Note(g', 4), Note(c', 8))
   '''

   tuplet = score[0][0].leaves
   treble = piano_staff[0].leaves
   bass = piano_staff[1].leaves

   assert set(moments[0].leaves) == set((tuplet[0], treble[0], bass[0]))
   assert set(moments[1].leaves) == set((tuplet[0], treble[0], bass[1]))
   assert set(moments[2].leaves) == set((tuplet[1], treble[0], bass[1]))
   assert set(moments[3].leaves) == set((tuplet[1], treble[1], bass[2]))
   assert set(moments[4].leaves) == set((tuplet[2], treble[1], bass[2]))
   assert set(moments[5].leaves) == set((tuplet[2], treble[1], bass[3]))


def test_iterate_vertical_moments_forward_in_expr_02( ):

   score = Score([ ])
   score.append(Staff([FixedDurationTuplet((4, 8), leaftools.make_repeated_notes(3))]))
   piano_staff = PianoStaff([ ])
   piano_staff.append(Staff(leaftools.make_repeated_notes(2, Rational(1, 4))))
   piano_staff.append(Staff(leaftools.make_repeated_notes(4)))
   piano_staff[1].clef.forced = Clef('bass')
   score.append(piano_staff)
   pitchtools.diatonicize(list(reversed(score.leaves)))

   ## see above for formatted score ##

   moment_generator = iterate.vertical_moments_forward_in_expr(piano_staff)
   moments = list(moment_generator)

   r'''
   (Note(a', 4), Note(f', 8))
   (Note(a', 4), Note(e', 8))
   (Note(g', 4), Note(d', 8))
   (Note(g', 4), Note(c', 8))
   '''

   treble = piano_staff[0].leaves
   bass = piano_staff[1].leaves

   assert set(moments[0].leaves) == set((treble[0], bass[0]))
   assert set(moments[1].leaves) == set((treble[0], bass[1]))
   assert set(moments[2].leaves) == set((treble[1], bass[2]))
   assert set(moments[3].leaves) == set((treble[1], bass[3]))
