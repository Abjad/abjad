from abjad.rational import Rational


def token_unpack(duration_token):
   '''Return reduced numerator, denominator pair from `duration_token`.

   Rationals are allowed. ::

      abjad> durtools.token_unpack(Rational(1, 4))
      (1, 4)

   Two-element integer tuples and lists are allowed. ::

      abjad> durtools.token_unpack((1, 4))
      (1, 4)
      abjad> durtools.token_unpack([1, 4])

   One-element integer tuples and lists are allowed. ::

      abjad> durtools.token_unpack((2, ))
      (2, 1)
      abjad> durtools.token_unpack([2])
      (2, 1)

   Integers are allowed. ::

      abjad> durtools.token_unpack(2)
      (2, 1)
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
   else:
      raise ValueError('token must be of tuple, list, int or Rational.')

   return numerator, denominator 
