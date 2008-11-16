from abjad.rational.rational import Rational


def _duration_token_unpack(duration_token):
   '''Return numerator, denominator pair from duration token,
      where duration token is an integer or a one- or two-element tuple;
      allow binary, nonbinary and all other duration tokens.'''

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
      numerator, denominator = duration_token.pair
   else:
      raise ValueError('duration token must be of type tuple, list, int or Rational.')

   return numerator, denominator 
