from abjad.helpers.least_multiple_greater import _least_multiple_greater
from abjad import *


def test_least_multiple_greater_01( ):
   '''Return the least multiple of m greater than or equal to n.'''

   assert _least_multiple_greater(10, 0) == 0
   assert _least_multiple_greater(10, 1) == 10
   assert _least_multiple_greater(10, 2) == 10
   assert _least_multiple_greater(10, 13) == 20
   assert _least_multiple_greater(10, 28) == 30
   assert _least_multiple_greater(10, 40) == 40
   assert _least_multiple_greater(10, 41) == 50
   

def test_least_multiple_greater_02( ):
   '''Return the least multiple of m greater than or equal to n.'''

   assert _least_multiple_greater(7, 0) == 0
   assert _least_multiple_greater(7, 1) == 7
   assert _least_multiple_greater(7, 2) == 7
   assert _least_multiple_greater(7, 13) == 14
   assert _least_multiple_greater(7, 28) == 28
   assert _least_multiple_greater(7, 40) == 42
   assert _least_multiple_greater(7, 41) == 42
