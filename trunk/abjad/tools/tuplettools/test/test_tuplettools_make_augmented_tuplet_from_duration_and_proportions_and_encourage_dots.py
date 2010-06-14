from abjad import *


def test_tuplettools_make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots_01( ):

   duration = Rational(3, 16)

   t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1])
   assert t.format == "{\n\tc'8.\n}"

   t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1, 1])
   assert t.format == "{\n\tc'16.\n\tc'16.\n}"

   t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1, 1, 1])
   assert t.format == "{\n\tc'16\n\tc'16\n\tc'16\n}"

   t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(
      duration, [1, 1, 1, 1])
   assert t.format == "{\n\tc'32.\n\tc'32.\n\tc'32.\n\tc'32.\n}"

   t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(
      duration, [1, 1, 1, 1, 1])
   assert t.format == "\\fraction \\times 8/5 {\n\tc'64.\n\tc'64.\n\tc'64.\n\tc'64.\n\tc'64.\n}" 


def test_tuplettools_make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots_02( ):

   duration = Rational(3, 16)

   t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1])
   assert t.format == "{\n\tc'8.\n}"

   t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1, 2])
   assert t.format == "{\n\tc'16\n\tc'8\n}"

   t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(duration, [1, 2, 2])
   assert t.format == "\\fraction \\times 8/5 {\n\tc'64.\n\tc'32.\n\tc'32.\n}" 

   t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(
      duration, [1, 2, 2, 3])
   assert t.format == "\\fraction \\times 3/2 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n}"

   t = tuplettools.make_augmented_tuplet_from_duration_and_proportions_and_encourage_dots(
      duration, [1, 2, 2, 3, 3])
   assert t.format == "\\fraction \\times 12/11 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n\tc'32.\n}"
