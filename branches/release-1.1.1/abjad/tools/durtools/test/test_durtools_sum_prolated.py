from abjad import *


def test_durtools_sum_prolated_01( ):
   '''Sum of prolated durations of components in list.'''

   t = FixedDurationTuplet((2, 8), construct.scale(3))

   assert durtools.sum_prolated(t.leaves) == Rational(2, 8)
