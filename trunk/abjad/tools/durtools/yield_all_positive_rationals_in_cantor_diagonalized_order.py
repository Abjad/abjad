from abjad.core import Fraction
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
      Fraction(1, 1)
      Fraction(2, 1)
      Fraction(1, 2)
      Fraction(1, 3)
      Fraction(1, 1)
      Fraction(3, 1)
      Fraction(4, 1)
      Fraction(3, 2)
      Fraction(2, 3)
      Fraction(1, 4)
      Fraction(1, 5)
      Fraction(1, 2)
      Fraction(1, 1)
      Fraction(2, 1)
      Fraction(5, 1)
      Fraction(6, 1)

   .. versionchanged:: 1.1.2
      renamed ``durtools.diagonalize_all_rationals( )`` to
      ``durtools.yield_all_positive_rationals_in_cantor_diagonalized_order( )``.
   '''

   generator = yield_all_positive_integer_pairs_in_cantor_diagonalized_order( )
   while True:
      integer_pair = generator.next( )
      rational = Fraction(*integer_pair)
      yield rational 
