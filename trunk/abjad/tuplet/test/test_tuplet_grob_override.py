from abjad import *


def test_tuplet_grob_override_01( ):
   '''Abjad tuplets wrap grob overrides at before and after.'''

   t = FixedDurationTuplet((2, 8), scale(3))
   t.tupletnumber.fraction = True

   r'''\override TupletNumber #'fraction = ##t
   \times 2/3 {
           c'8
           d'8
           e'8
   }
   \revert TupletNumber #'fraction'''

   assert check.wf(t)
   assert t.format == "\\override TupletNumber #'fraction = ##t\n\\times 2/3 {\n\tc'8\n\td'8\n\te'8\n}\n\\revert TupletNumber #'fraction"
