from abjad import *


def test_mathtools_integer_partitions_01( ):
   '''Yield all integer partitions of positive integer n
   in descending lex order.'''

   partitions = mathtools.integer_partitions(7)
   partitions = list(partitions)

   assert partitions[0] == (7,)
   assert partitions[1] == (6, 1)
   assert partitions[2] == (5, 2)
   assert partitions[3] == (5, 1, 1)
   assert partitions[4] == (4, 3)
   assert partitions[5] == (4, 2, 1)
   assert partitions[6] == (4, 1, 1, 1)
   assert partitions[7] == (3, 3, 1)
   assert partitions[8] == (3, 2, 2)
   assert partitions[9] == (3, 2, 1, 1)
   assert partitions[10] == (3, 1, 1, 1, 1)
   assert partitions[11] == (2, 2, 2, 1)
   assert partitions[12] == (2, 2, 1, 1, 1)
   assert partitions[13] == (2, 1, 1, 1, 1, 1)
   assert partitions[14] == (1, 1, 1, 1, 1, 1, 1)
