from abjad.rational import Rational
from abjad.tools.durtools.diagonalize_all_positive_integer_pairs import \
   diagonalize_all_positive_integer_pairs


def diagonalize_all_rationals( ):
   r'''.. versionadded:: 1.1.2

   Cantor diagonalization of the rationals.
   
   Values appear multiple times. ::

      abjad> generator = durtools.diagonalize_all_rationals( )
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
   '''

   generator = diagonalize_all_positive_integer_pairs( )
   while True:
      integer_pair = generator.next( )
      rational = Rational(*integer_pair)
      yield rational 
