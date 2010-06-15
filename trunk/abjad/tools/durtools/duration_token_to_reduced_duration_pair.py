from abjad.rational import Rational
from abjad.tools.durtools.lilypond_duration_string_to_rational import \
   lilypond_duration_string_to_rational


def duration_token_to_reduced_duration_pair(duration_token):
   '''Return reduced numerator, denominator pair equal to `duration_token`.

   Rationals are allowed. ::

      abjad> durtools.duration_token_to_reduced_duration_pair(Rational(1, 4))
      (1, 4)

   Two-element integer tuples and lists are allowed. ::

      abjad> durtools.duration_token_to_reduced_duration_pair((1, 4))
      (1, 4)
      abjad> durtools.duration_token_to_reduced_duration_pair([1, 4])

   One-element integer tuples and lists are allowed. ::

      abjad> durtools.duration_token_to_reduced_duration_pair((2, ))
      (2, 1)
      abjad> durtools.duration_token_to_reduced_duration_pair([2])
      (2, 1)

   Integers are allowed. ::

      abjad> durtools.duration_token_to_reduced_duration_pair(2)
      (2, 1)

   .. versionadded:: 1.1.2
      LilyPond-style duration strings are allowed.

   ::

      abjad> durtools.duration_token_to_reduced_duration_pair('8.')
      (3, 16)

   .. versionchanged:: 1.1.2
      renamed ``durtools.token_unpack( )`` to
      ``durtools.duration_token_to_reduced_duration_pair( )``.
   '''

   if isinstance(duration_token, (tuple, list)):
      if len(duration_token) == 1:
         numerator = duration_token[0]
         denominator = 1
      elif len(duration_token) == 2:
         numerator, denominator = duration_token
      else:
         raise ValueError('duration tuple must be of length 1 or 2.')
   elif isinstance(duration_token, int):
      numerator = duration_token
      denominator = 1
   elif isinstance(duration_token, Rational):
      numerator, denominator = duration_token._n, duration_token._d
   elif isinstance(duration_token, str):
      rational = lilypond_duration_string_to_rational(duration_token)
      numerator, denominator = rational._n, rational._d
   else:
      raise TypeError('token must be of tuple, list, int or Rational.')

   return numerator, denominator 
