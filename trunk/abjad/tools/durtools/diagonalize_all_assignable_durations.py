from abjad.tools.durtools.diagonalize_all_rationals_unique import \
   diagonalize_all_rationals_unique
from abjad.tools.durtools.is_assignable import is_assignable as \
   durtools_is_assignable


def diagonalize_all_assignable_durations( ):
   '''.. versionadded:: 1.1.2

   Cantor diagonalization of all note-head-assignable durations. ::

      abjad> generator = durtools.diagonalize_all_assignable_durations( )
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
   '''


   generator = diagonalize_all_rationals_unique( )
   while True:
      duration = generator.next( )
      if durtools_is_assignable(duration):
         yield duration
