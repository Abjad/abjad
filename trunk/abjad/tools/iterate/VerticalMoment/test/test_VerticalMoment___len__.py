from abjad import *


def test_VerticalMoment___len___01( ):

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

   vertical_moment = iterate.get_vertical_moment_at_prolated_offset_in(
      score, Rational(1, 8))
   "VerticalMoment(Score<<2>>, Staff{1}, {@ 3:4 d''8, c''8, b'8 @}, d''8, PianoStaff<<2>>, Staff{2}, a'4, Staff{4}, e'8)"
   assert len(vertical_moment) == 9

   vertical_moment = iterate.get_vertical_moment_at_prolated_offset_in(
      score[0], Rational(1, 8))
   "VerticalMoment(Staff{1}, {@ 3:4 d''8, c''8, b'8 @}, d''8)"
   assert len(vertical_moment) == 3

   vertical_moment = iterate.get_vertical_moment_at_prolated_offset_in(
      piano_staff, Rational(1, 8))
   "VerticalMoment(PianoStaff<<2>>, Staff{2}, a'4, Staff{4}, e'8)"
   assert len(vertical_moment) == 5

   vertical_moment = iterate.get_vertical_moment_at_prolated_offset_in(
      piano_staff[0], Rational(1, 8))
   "VerticalMoment(Staff{2}, a'4)"
   assert len(vertical_moment) == 2

   vertical_moment = iterate.get_vertical_moment_at_prolated_offset_in(
      piano_staff[1], Rational(1, 8))
   "VerticalMoment(Staff{2}, e'8)"
   assert len(vertical_moment) == 2
