from abjad.tools.durtools.yield_all_positive_rationals_in_cantor_diagonalized_order_uniquely \
   import yield_all_positive_rationals_in_cantor_diagonalized_order_uniquely
from abjad.tools.durtools.is_assignable_rational import is_assignable_rational


def yield_all_assignable_rationals_in_cantor_diagonalized_order( ):
   '''.. versionadded:: 1.1.2

   Yield all assignable rationals in Cantor diagonalized order::

      abjad> generator = durtools.yield_all_assignable_rationals_in_cantor_diagonalized_order( )
      abjad> for n in range(16):
      ...     generator.next( )
      ... 
      Fraction(1, 1)
      Fraction(2, 1)
      Fraction(1, 2)
      Fraction(3, 1)
      Fraction(4, 1)
      Fraction(3, 2)
      Fraction(1, 4)
      Fraction(6, 1)
      Fraction(3, 4)
      Fraction(7, 1)
      Fraction(8, 1)
      Fraction(7, 2)
      Fraction(1, 8)
      Fraction(7, 4)
      Fraction(3, 8)
      Fraction(12, 1)

   Return fraction generator.
   '''


   generator = yield_all_positive_rationals_in_cantor_diagonalized_order_uniquely( )
   while True:
      duration = generator.next( )
      if is_assignable_rational(duration):
         yield duration
