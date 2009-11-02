from abjad import *


def test_divide_leaf_into_arbitrary_augmentation_01( ):

   note = Note(0, (3, 16))

   t = divide.leaf_into_arbitrary_augmentation(note, [1])
   assert t.format == "\tc'8."

   t = divide.leaf_into_arbitrary_augmentation(note, [1, 2])
   assert t.format == "\tc'16\n\tc'8"

   t = divide.leaf_into_arbitrary_augmentation(note, [1, 2, 2])
   assert t.format == "\\fraction \\times 6/5 {\n\tc'32\n\tc'16\n\tc'16\n}"

   t = divide.leaf_into_arbitrary_augmentation(note, [1, 2, 2, 3])
   assert t.format == "\\fraction \\times 3/2 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n}"

   t = divide.leaf_into_arbitrary_augmentation(note, [1, 2, 2, 3, 3])
   assert t.format == "\\fraction \\times 12/11 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n\tc'32.\n}"

   t = divide.leaf_into_arbitrary_augmentation(note, [1, 2, 2, 3, 3, 4])
   assert t.format == "\\times 8/5 {\n\tc'128\n\tc'64\n\tc'64\n\tc'64.\n\tc'64.\n\tc'32\n}"
