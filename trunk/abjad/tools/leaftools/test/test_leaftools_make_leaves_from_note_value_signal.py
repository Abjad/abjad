from abjad import *


def test_leaftools_make_leaves_from_note_value_signal_01( ):

   leaves = leaftools.make_leaves_from_note_value_signal([2, -2, 3, -3], Fraction(1, 8))
   staff = Staff(leaves)

   r'''
   \new Staff {
      c'4
      r4
      c'4.
      r4.
   }
   '''

   assert staff.format == "\\new Staff {\n\tc'4\n\tr4\n\tc'4.\n\tr4.\n}"
