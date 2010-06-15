from abjad import *


def test_durtools_yield_all_assignable_rationals_in_cantor_diagonalized_order_01( ):

   generator = durtools.yield_all_assignable_rationals_in_cantor_diagonalized_order( )

   assert generator.next( ) == Rational(1, 1)
   assert generator.next( ) == Rational(2, 1)
   assert generator.next( ) == Rational(1, 2)
   assert generator.next( ) == Rational(3, 1)
   assert generator.next( ) == Rational(4, 1)
   assert generator.next( ) == Rational(3, 2)
   assert generator.next( ) == Rational(1, 4)
   assert generator.next( ) == Rational(6, 1)
   assert generator.next( ) == Rational(3, 4)
   assert generator.next( ) == Rational(7, 1)
   assert generator.next( ) == Rational(8, 1)
   assert generator.next( ) == Rational(7, 2)
   assert generator.next( ) == Rational(1, 8)
   assert generator.next( ) == Rational(7, 4)
   assert generator.next( ) == Rational(3, 8)
   assert generator.next( ) == Rational(12, 1)
