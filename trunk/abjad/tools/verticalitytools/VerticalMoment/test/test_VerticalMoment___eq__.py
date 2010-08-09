from abjad import *


def test_VerticalMoment___eq___01( ):

   score = Score([ ])
   score.append(Staff([FixedDurationTuplet((4, 8), leaftools.make_repeated_notes(3))]))
   piano_staff = PianoStaff([ ])
   piano_staff.append(Staff(leaftools.make_repeated_notes(2, Rational(1, 4))))
   piano_staff.append(Staff(leaftools.make_repeated_notes(4)))
   piano_staff[1].clef.forced = Clef('bass')
   score.append(piano_staff)
   pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(list(reversed(score.leaves)))

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

   vertical_moment_1 = iterate.get_vertical_moment_at_prolated_offset_in_expr(
      piano_staff, Rational(1, 8))

   "VerticalMoment(PianoStaff<<2>>, Staff{2}, a'4, Staff{4}, e'8)"

   vertical_moment_2 = iterate.get_vertical_moment_at_prolated_offset_in_expr(
      piano_staff, Rational(1, 8))

   "VerticalMoment(PianoStaff<<2>>, Staff{2}, a'4, Staff{4}, e'8)"

   assert vertical_moment_1 == vertical_moment_2
   assert not vertical_moment_1 != vertical_moment_2


def test_VerticalMoment___eq___02( ):

   score = Score([ ])
   score.append(Staff([FixedDurationTuplet((4, 8), leaftools.make_repeated_notes(3))]))
   piano_staff = PianoStaff([ ])
   piano_staff.append(Staff(leaftools.make_repeated_notes(2, Rational(1, 4))))
   piano_staff.append(Staff(leaftools.make_repeated_notes(4)))
   piano_staff[1].clef.forced = Clef('bass')
   score.append(piano_staff)
   pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(list(reversed(score.leaves)))

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

   vertical_moment_1 = iterate.get_vertical_moment_at_prolated_offset_in_expr(
      piano_staff, Rational(1, 8))

   "VerticalMoment(PianoStaff<<2>>, Staff{2}, a'4, Staff{4}, e'8)"

   vertical_moment_2 = iterate.get_vertical_moment_at_prolated_offset_in_expr(
      (piano_staff[0], piano_staff[1]), Rational(1, 8))

   "VerticalMoment(Staff{2}, a'4, Staff{4}, e'8)"

   assert not vertical_moment_1 == vertical_moment_2
   assert vertical_moment_1 != vertical_moment_2
