from abjad import *


def test_system_y_offsets_01( ):

   y = SystemYOffsets(44, 5)
   assert str(y) == 'SystemYOffsets([0], 44, 88, 132, 176 | 0, 44, 88, 132, 176 | ...)'
