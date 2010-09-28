from abjad import *


def test_Rest___eq___01( ):

   rest_1 = Rest((1, 4))
   rest_2 = Rest((1, 4))
   rest_3 = Rest((1, 8))

   assert     rest_1 == rest_2
   assert not rest_1 == rest_3
   assert not rest_2 == rest_3
