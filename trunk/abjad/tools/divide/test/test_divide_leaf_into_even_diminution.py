from abjad import *


def test_divide_leaf_into_even_diminution_01( ):
   '''Divide a leaf of 3/16 into 1, ..., 5 parts.'''

   t = divide.leaf_into_even_diminution(Note(0, (3, 16)), 1)
   assert t.format == "\tc'8."

   t = divide.leaf_into_even_diminution(Note(0, (3, 16)), 2)
   assert t.format == "\tc'16.\n\tc'16."

   t = divide.leaf_into_even_diminution(Note(0, (3, 16)), 3)
   assert t.format == "\tc'16\n\tc'16\n\tc'16"

   t = divide.leaf_into_even_diminution(Note(0, (3, 16)), 4)
   assert t.format == "\tc'32.\n\tc'32.\n\tc'32.\n\tc'32."

   t = divide.leaf_into_even_diminution(Note(0, (3, 16)), 5)
   assert t.format == "\\fraction \\times 3/5 {\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n}"
