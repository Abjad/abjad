from abjad import *


def test_mathtools_least_common_multiple_01( ):

   assert mathtools.least_common_multiple(4, 4) == 4
   assert mathtools.least_common_multiple(4, 5) == 20
   assert mathtools.least_common_multiple(4, 6) == 12
   assert mathtools.least_common_multiple(4, 7) == 28
   assert mathtools.least_common_multiple(4, 8) == 8
   assert mathtools.least_common_multiple(4, 9) == 36
   assert mathtools.least_common_multiple(4, 10) == 20
   assert mathtools.least_common_multiple(4, 11) == 44
