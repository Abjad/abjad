from abjad import *


def test_divide_leaf_01( ):
   '''Divide a leaf of 3/16 into 1, ..., 5 parts, by diminution.'''

   t = divide.leaf(Note(0, (3, 16)), 1, 'diminution')
   assert t.format == "\tc'8."

   t = divide.leaf(Note(0, (3, 16)), 2, 'diminution')
   assert t.format == "\tc'16.\n\tc'16."

   t = divide.leaf(Note(0, (3, 16)), 3, 'diminution')
   assert t.format == "\tc'16\n\tc'16\n\tc'16"

   t = divide.leaf(Note(0, (3, 16)), 4, 'diminution')
   assert t.format == "\tc'32.\n\tc'32.\n\tc'32.\n\tc'32."

   t = divide.leaf(Note(0, (3, 16)), 5, 'diminution')
   assert t.format == "\\fraction \\times 3/5 {\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n}"


def test_divide_leaf_02( ):
   '''Divide a leaf of 3/16 into 1, ..., 5 parts, by augmentation.'''

   t = divide.leaf(Note(0, (3, 16)), 1, 'augmentation')
   assert t.format == "\tc'8."

   t = divide.leaf(Note(0, (3, 16)), 2, 'augmentation')
   assert t.format == "\tc'16.\n\tc'16."

   t = divide.leaf(Note(0, (3, 16)), 3, 'augmentation')
   assert t.format == "\tc'16\n\tc'16\n\tc'16"

   t = divide.leaf(Note(0, (3, 16)), 4, 'augmentation')
   assert t.format == "\tc'32.\n\tc'32.\n\tc'32.\n\tc'32."

   t = divide.leaf(Note(0, (3, 16)), 5, 'augmentation')
   assert t.format == "\\fraction \\times 6/5 {\n\tc'32\n\tc'32\n\tc'32\n\tc'32\n\tc'32\n}"
