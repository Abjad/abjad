from abjad import *


def test_divide_duration_into_arbitrary_augmentation_undotted_01( ):

   duration = Rational(3, 16)

   t = divide.duration_into_arbitrary_augmentation_undotted(duration, [1])
   assert t.format == "\\fraction \\times 3/2 {\n\tc'8\n}"

   t = divide.duration_into_arbitrary_augmentation_undotted(duration, [1, 1])
   assert t.format == "\\fraction \\times 3/2 {\n\tc'16\n\tc'16\n}"

   t = divide.duration_into_arbitrary_augmentation_undotted(duration, [1, 1, 1])
   assert t.format == "\tc'16\n\tc'16\n\tc'16"

   t = divide.duration_into_arbitrary_augmentation_undotted(
      duration, [1, 1, 1, 1])
   assert t.format == "\\fraction \\times 3/2 {\n\tc'32\n\tc'32\n\tc'32\n\tc'32\n}"

   t = divide.duration_into_arbitrary_augmentation_undotted(
      duration, [1, 1, 1, 1, 1])
   assert t.format == "\\fraction \\times 6/5 {\n\tc'32\n\tc'32\n\tc'32\n\tc'32\n\tc'32\n}"


def test_divide_duration_into_arbitrary_augmentation_undotted_02( ):

   duration = Rational(3, 16)

   t = divide.duration_into_arbitrary_augmentation_undotted(duration, [1])
   assert t.format == "\\fraction \\times 3/2 {\n\tc'8\n}"

   t = divide.duration_into_arbitrary_augmentation_undotted(duration, [1, 2])
   assert t.format == "\tc'16\n\tc'8"

   t = divide.duration_into_arbitrary_augmentation_undotted(duration, [1, 2, 2])
   assert t.format == "\\fraction \\times 6/5 {\n\tc'32\n\tc'16\n\tc'16\n}"

   t = divide.duration_into_arbitrary_augmentation_undotted(
      duration, [1, 2, 2, 3])
   assert t.format == "\\fraction \\times 3/2 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n}"

   t = divide.duration_into_arbitrary_augmentation_undotted(
      duration, [1, 2, 2, 3, 3])
   assert t.format == "\\fraction \\times 12/11 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n\tc'32.\n}"
