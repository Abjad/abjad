from abjad.core import Rational
from abjad.tools.durtools.yield_all_positive_integer_pairs_in_cantor_diagonalized_order import \
   yield_all_positive_integer_pairs_in_cantor_diagonalized_order


def yield_all_positive_rationals_in_cantor_diagonalized_order( ):
   r'''.. versionadded:: 1.1.2

   Cantor diagonalization of the rationals.
   
   Values appear multiple times. ::

      abjad> generator = durtools.yield_all_positive_rationals_in_cantor_diagonalized_order( )
      abjad> for n in range(16):
      ...     generator.next( )
      ... 
      Rational(1, 1)
      Rational(2, 1)
      Rational(1, 2)
      Rational(1, 3)
      Rational(1, 1)
      Rational(3, 1)
      Rational(4, 1)
      Rational(3, 2)
      Rational(2, 3)
      Rational(1, 4)
      Rational(1, 5)
      Rational(1, 2)
      Rational(1, 1)
      Rational(2, 1)
      Rational(5, 1)
      Rational(6, 1)

   .. versionchanged:: 1.1.2
      renamed ``durtools.diagonalize_all_rationals( )`` to
      ``durtools.yield_all_positive_rationals_in_cantor_diagonalized_order( )``.
   '''

   generator = yield_all_positive_integer_pairs_in_cantor_diagonalized_order( )
   while True:
      integer_pair = generator.next( )
      rational = Rational(*integer_pair)
      yield rational 
