from abjad.tools.durtools.duration_token_to_duration_pair import duration_token_to_duration_pair
from fractions import Fraction


def duration_token_to_rational(duration_token):
   '''.. versionadded:: 1.1.2

   Change `duration_token` to rational::

      abjad> from abjad.tools import durtools

   ::

      abjad> durtools.duration_token_to_rational((4, 16))
      Fraction(1, 4)

   ::

      abjad> durtools.duration_token_to_rational('4.')
      Fraction(3, 8)

   Return fraction.
   '''

   return Fraction(*duration_token_to_duration_pair(duration_token))
