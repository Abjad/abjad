from abjad import *


def test_divide_leaf_into_even_augmentation_01( ):
   '''Divide a leaf of 3/16 into 1, ..., 5 parts.'''

   t = divide.leaf_into_even_augmentation(Note(0, (3, 16)), 1)
   assert t.format == "{\n\tc'8.\n}"

   t = divide.leaf_into_even_augmentation(Note(0, (3, 16)), 2)
   assert t.format == "{\n\tc'16.\n\tc'16.\n}"

   t = divide.leaf_into_even_augmentation(Note(0, (3, 16)), 3)
   assert t.format == "{\n\tc'16\n\tc'16\n\tc'16\n}"

   t = divide.leaf_into_even_augmentation(Note(0, (3, 16)), 4)
   assert t.format == "{\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n}"

   t = divide.leaf_into_even_augmentation(Note(0, (3, 16)), 5)
   #assert t.format == "\\fraction \\times 6/5 {\n\tc'32\n\tc'32\n\tc'32\n\tc'32\n\tc'32\n}"
   assert t.format == "\\times 8/5 {\n\tc'64.\n\tc'64.\n\tc'64.\n\tc'64.\n\tc'64.\n}"
