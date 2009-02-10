from abjad import *


def test_tcopy_notes_in_tuplet_01( ):
   '''Copy notes from tuplet and preserve tuplet target duration.'''

   t = FixedDurationTuplet((4, 8), scale(5))
   u = tcopy(t[:3])

   r'''
   \times 4/5 {
           c'8
           d'8
           e'8
   }
   '''

   assert isinstance(u, FixedDurationTuplet)
   assert u.duration.target == Rational(3, 10)
   assert len(u) == 3

   assert u.format == "\\times 4/5 {\n\tc'8\n\td'8\n\te'8\n}"
