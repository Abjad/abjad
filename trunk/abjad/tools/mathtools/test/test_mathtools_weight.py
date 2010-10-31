from abjad import *


def test_mathtools_weight_01( ):
   '''Weight of nonempty sequence.
   '''

   assert mathtools.weight([-1, -2, 3, 4, 5]) == 15


def test_mathtools_weight_02( ):
   '''Weight of empty sequence.
   '''

   assert mathtools.weight([ ]) == 0
