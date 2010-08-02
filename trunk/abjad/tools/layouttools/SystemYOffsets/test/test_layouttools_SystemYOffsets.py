from abjad import *


def test_layouttools_SystemYOffsets_01( ):

   y = layouttools.SystemYOffsets(44, 5)
   assert str(y) == 'SystemYOffsets([0], 44, 88, 132, 176 | 0, 44, 88, 132, 176 | ...)'
