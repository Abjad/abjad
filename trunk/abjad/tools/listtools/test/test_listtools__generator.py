from abjad import *


def test_listtools__generator_01( ):
   '''Same arguments as built-in range( ).'''

   g = listtools._generator(1, 8)
   
   assert list(g) == [1, 2, 3, 4, 5, 6, 7]
