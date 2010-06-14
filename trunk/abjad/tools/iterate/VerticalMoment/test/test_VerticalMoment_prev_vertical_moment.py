from abjad import *


def test_VerticalMoment_prev_vertical_moment_01( ):

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

   last_leaf = score.leaves[-1]
   vertical_moment = iterate.get_vertical_moment_starting_with(last_leaf)
   assert vertical_moment.prolated_offset == Rational(3, 8)

   vertical_moment = vertical_moment.prev_vertical_moment
   assert vertical_moment.prolated_offset == Rational(1, 3)

   vertical_moment = vertical_moment.prev_vertical_moment
   assert vertical_moment.prolated_offset == Rational(1, 4)

   vertical_moment = vertical_moment.prev_vertical_moment
   assert vertical_moment.prolated_offset == Rational(1, 6)

   vertical_moment = vertical_moment.prev_vertical_moment
   assert vertical_moment.prolated_offset == Rational(1, 8)

   vertical_moment = vertical_moment.prev_vertical_moment
   assert vertical_moment.prolated_offset == Rational(0)
