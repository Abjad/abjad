from abjad import *


def test_leaftools_get_durations_written_01( ):

   staff = Staff(FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3)) * 2)
   durations = leaftools.get_durations_written(staff)

   assert durations == [Rational(1, 8), Rational(1, 8), Rational(1, 8), 
      Rational(1, 8), Rational(1, 8), Rational(1, 8)]
