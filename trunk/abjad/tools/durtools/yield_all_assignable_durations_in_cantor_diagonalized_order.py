from abjad.tools.durtools.yield_all_unique_positive_rationals_in_cantor_diagonalized_order import \
   yield_all_unique_positive_rationals_in_cantor_diagonalized_order
from abjad.tools.durtools.is_assignable_rational import is_assignable_rational


def yield_all_assignable_durations_in_cantor_diagonalized_order( ):
   '''.. versionadded:: 1.1.2

   Cantor diagonalization of all note-head-assignable durations. ::

      abjad> generator = durtools.yield_all_assignable_durations_in_cantor_diagonalized_order( )
      abjad> for n in range(16):
      ...     generator.next( )
      ... 
      Rational(1, 1)
      Rational(2, 1)
      Rational(1, 2)
      Rational(3, 1)
      Rational(4, 1)
      Rational(3, 2)
      Rational(1, 4)
      Rational(6, 1)
      Rational(3, 4)
      Rational(7, 1)
      Rational(8, 1)
      Rational(7, 2)
      Rational(1, 8)
      Rational(7, 4)
      Rational(3, 8)
      Rational(12, 1)

   .. versionchanged:: 1.1.2
      renamed ``durtools.diagonalize_all_assignable_durations( )`` to
      ``durtools.yield_all_assignable_durations_in_cantor_diagonalized_order( )``.
   '''


   generator = yield_all_unique_positive_rationals_in_cantor_diagonalized_order( )
   while True:
      duration = generator.next( )
      if is_assignable_rational(duration):
         yield duration
