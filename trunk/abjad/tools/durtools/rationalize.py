from abjad.rational import Rational
from abjad.tools.durtools.is_duration_token import is_duration_token
from abjad.tools.durtools.token_unpack import token_unpack


def rationalize(duration_tokens):
   '''Convert nested `duration_tokens` to rationals.

   ::

      abjad> durtools.rationalize([(1, 16), (2, 16)])
      [Rational(1, 16), Rational(1, 8)]

   ::

      abjad> durtools.rationalize([(1, 16), [(2, 16), (3, 16)]])
      [Rational(1, 16), [Rational(1, 8), Rational(3, 16)]]
   '''

   assert isinstance(duration_tokens, list)
   result = [ ]
   for element in duration_tokens:
      if is_duration_token(element):
         r = Rational(*token_unpack(element))
      else:
         r = rationalize(element)
      result.append(r)
   return result
