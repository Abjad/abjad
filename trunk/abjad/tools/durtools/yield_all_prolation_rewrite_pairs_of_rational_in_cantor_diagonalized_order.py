from abjad.Rational import Rational
from abjad.tools.durtools.yield_all_assignable_rationals_in_cantor_diagonalized_order import \
   yield_all_assignable_rationals_in_cantor_diagonalized_order


def yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order(
   prolated_duration, minimum_written_duration = Rational(1, 128)):
   r'''.. versionadded:: 1.1.2

   Return tuple of the different ways to notate `prolated_duration`
   as prolation, written pairs.

   Ensure written duration never less than `minimum_written_duration`.

   The different ways to notate a prolated duration of ``1/8``. ::

      abjad> pairs = durtools.yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order(Rational(1, 8))
      abjad> for pair in pairs: pair
      ... 
      (Rational(1, 1), Rational(1, 8))
      (Rational(2, 3), Rational(3, 16))
      (Rational(4, 3), Rational(3, 32))
      (Rational(4, 7), Rational(7, 32))
      (Rational(8, 7), Rational(7, 64))
      (Rational(8, 15), Rational(15, 64))
      (Rational(16, 15), Rational(15, 128))
      (Rational(16, 31), Rational(31, 128))

   The different ways to notate a prolated duration of ``1/12``. ::

      abjad> pairs = durtools.yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order(Rational(1, 12))
      abjad> for pair in pairs: pair
      ... 
      (Rational(2, 3), Rational(1, 8))
      (Rational(4, 3), Rational(1, 16))
      (Rational(8, 9), Rational(3, 32))
      (Rational(16, 9), Rational(3, 64))
      (Rational(16, 21), Rational(7, 64))
      (Rational(32, 21), Rational(7, 128))
      (Rational(32, 45), Rational(15, 128))

   The different ways to notate a prolated duration of ``5/48``. ::

      abjad> pairs = durtools.yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order(Rational(5, 48))
      abjad> for pair in pairs: pair
      ... 
      (Rational(5, 6), Rational(1, 8))
      (Rational(5, 3), Rational(1, 16))
      (Rational(5, 9), Rational(3, 16))
      (Rational(10, 9), Rational(3, 32))
      (Rational(20, 21), Rational(7, 64))
      (Rational(40, 21), Rational(7, 128))
      (Rational(8, 9), Rational(15, 128))      

   .. versionchanged:: 1.1.2
      renamed ``durtools.prolated_to_prolation_written_pairs( )`` to
      ``durtools.yield_all_prolation_rewrite_pairs_of_rational_in_cantor_diagonalized_order( )``.
   '''
   from abjad.tools.tuplettools.is_proper_tuplet_multiplier import is_proper_tuplet_multiplier

   generator = yield_all_assignable_rationals_in_cantor_diagonalized_order( )
   pairs = [ ]

   while True:
      written_duration = generator.next( )
      if written_duration < minimum_written_duration:
         pairs = tuple(pairs)
         return pairs
      prolation = prolated_duration / written_duration
      if is_proper_tuplet_multiplier(prolation):
         pair = (prolation, written_duration)
         pairs.append(pair)
