from abjad import *


def test_fdtuplet_preferred_duration_01( ):

   t = FixedDurationTuplet((4, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(6))
   t.duration.preferred_denominator = 4

   r'''
   \times 4/6 {
           c'8
           d'8
           e'8
           f'8
           g'8
           a'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\times 4/6 {\n\tc'8\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8\n}"
