from abjad import *


def test_durtools_diagonalize_all_rationals_01( ):

   generator = durtools.diagonalize_all_rationals( )

   assert generator.next( ) == Rational(1, 1)
   assert generator.next( ) == Rational(2, 1)
   assert generator.next( ) == Rational(1, 2)
   assert generator.next( ) == Rational(1, 3)
   assert generator.next( ) == Rational(1, 1)
   assert generator.next( ) == Rational(3, 1)
   assert generator.next( ) == Rational(4, 1)
   assert generator.next( ) == Rational(3, 2)
   assert generator.next( ) == Rational(2, 3)
   assert generator.next( ) == Rational(1, 4)
   assert generator.next( ) == Rational(1, 5)
   assert generator.next( ) == Rational(1, 2)
   assert generator.next( ) == Rational(1, 1)
   assert generator.next( ) == Rational(2, 1)
   assert generator.next( ) == Rational(5, 1)
   assert generator.next( ) == Rational(6, 1)
