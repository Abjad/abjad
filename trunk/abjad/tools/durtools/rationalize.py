from abjad.rational import Rational
from abjad.tools.durtools.is_token import is_token
from abjad.tools.durtools.token_unpack import token_unpack


def rationalize(l):
   '''Convert duration tokens in `l` to rationals.

   ::

      abjad> durtools.rationalize([(1, 16), (2, 16)])
      [Rational(1, 16), Rational(1, 8)]

   `l` may be nested. ::

      abjad> durtools.rationalize([(1, 16), [(2, 16), (3, 16)]])
      [Rational(1, 16), [Rational(1, 8), Rational(3, 16)]]
   '''

   assert isinstance(l, list)
   result = [ ]
   for element in l:
      if is_token(element):
         r = Rational(*token_unpack(element))
      else:
         r = rationalize(element)
      result.append(r)
   return result
