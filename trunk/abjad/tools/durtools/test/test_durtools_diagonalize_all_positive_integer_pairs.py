from abjad import *


def test_durtools_diagonalize_all_positive_integer_pairs_01( ):
   
   generator = durtools.diagonalize_all_positive_integer_pairs( )

   assert generator.next( ) == (1, 1)
   assert generator.next( ) == (2, 1)
   assert generator.next( ) == (1, 2)
   assert generator.next( ) == (1, 3)
   assert generator.next( ) == (2, 2)
   assert generator.next( ) == (3, 1)
   assert generator.next( ) == (4, 1)
   assert generator.next( ) == (3, 2)
   assert generator.next( ) == (2, 3)
   assert generator.next( ) == (1, 4)
   assert generator.next( ) == (1, 5)
   assert generator.next( ) == (2, 4)
