from abjad import *


def test_iterate_get_vertical_moment_starting_with_component_01( ):

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

   def piano_staff_moment(expr):
      return iterate.get_vertical_moment_starting_with_component(expr, piano_staff)

   vm = piano_staff_moment(piano_staff[1][0])
   assert vm.leaves == (piano_staff[0][0], piano_staff[1][0])

   vm = piano_staff_moment(piano_staff[1][1])
   assert vm.leaves == (piano_staff[0][0], piano_staff[1][1])

   vm = piano_staff_moment(piano_staff[1][2])
   assert vm.leaves == (piano_staff[0][1], piano_staff[1][2])

   vm = piano_staff_moment(piano_staff[1][3])
   assert vm.leaves == (piano_staff[0][1], piano_staff[1][3])

   
def test_iterate_get_vertical_moment_starting_with_component_02( ):

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

   vm = iterate.get_vertical_moment_starting_with_component(piano_staff[1][0])
   assert vm.leaves == (score[0][0][0], piano_staff[0][0], piano_staff[1][0])

   vm = iterate.get_vertical_moment_starting_with_component(piano_staff[1][1])
   assert vm.leaves == (score[0][0][0], piano_staff[0][0], piano_staff[1][1])

   vm = iterate.get_vertical_moment_starting_with_component(piano_staff[1][2])
   assert vm.leaves == (score[0][0][1], piano_staff[0][1], piano_staff[1][2])

   vm = iterate.get_vertical_moment_starting_with_component(piano_staff[1][3])
   assert vm.leaves == (score[0][0][2], piano_staff[0][1], piano_staff[1][3])
