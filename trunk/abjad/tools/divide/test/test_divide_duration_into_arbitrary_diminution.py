from abjad import *


def test_divide_duration_into_arbitrary_diminution_01( ):

   duration = Rational(3, 16)

   t = divide.duration_into_arbitrary_diminution(duration, [1])
   assert t.format == "\tc'8."

   t = divide.duration_into_arbitrary_diminution(duration, [1, 2])
   assert t.format == "\tc'16\n\tc'8"

   ## TODO: DECIDE ON DOTTED VALUES ##
   #t = divide.duration_into_arbitrary_diminution(duration, [1, 2, 2])
   #assert t.format == "\\fraction \\times 3/5 {\n\tc'16\n\tc'8\n\tc'8\n}"

   t = divide.duration_into_arbitrary_diminution(duration, [1, 2, 2, 3])
   assert t.format == "\\fraction \\times 3/4 {\n\tc'32\n\tc'16\n\tc'16\n\tc'16.\n}"

   t = divide.duration_into_arbitrary_diminution(duration, [1, 2, 2, 3, 3])
   assert t.format == "\\fraction \\times 6/11 {\n\tc'32\n\tc'16\n\tc'16\n\tc'16.\n\tc'16.\n}"

   t = divide.duration_into_arbitrary_diminution(duration, [1, 2, 2, 3, 3, 4])
   assert t.format == "\\times 4/5 {\n\tc'64\n\tc'32\n\tc'32\n\tc'32.\n\tc'32.\n\tc'16\n}"
