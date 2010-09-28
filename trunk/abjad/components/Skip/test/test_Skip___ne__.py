from abjad import *


def test_Skip___ne___01( ):

   skip_1 = Skip((1, 4))
   skip_2 = Skip((1, 4))
   skip_3 = Skip((1, 8))

   assert not skip_1 != skip_2
   assert     skip_1 != skip_3
   assert     skip_2 != skip_3
