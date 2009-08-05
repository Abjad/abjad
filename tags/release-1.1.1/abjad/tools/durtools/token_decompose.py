from abjad.tools.durtools.token_unpack import token_unpack
from abjad.tools import mathtools


def token_decompose(duration_token):
   '''Return big-endian list of notehead-assignable duration tokens.

      abjad> duration_tokens = [(n, 16) for n in range(10, 20)]
      abjad> for duration_token in duration_tokens:
      ...     print duration_token, durtools.token_decompose(duration_token)
      ... 
      (10, 16) ((8, 16), (2, 16))
      (11, 16) ((8, 16), (3, 16))
      (12, 16) ((12, 16),)
      (13, 16) ((12, 16), (1, 16))
      (14, 16) ((14, 16),)
      (15, 16) ((15, 16),)
      (16, 16) ((16, 16),)
      (17, 16) ((16, 16), (1, 16))
      (18, 16) ((16, 16), (2, 16))
      (19, 16) ((16, 16), (3, 16))'''

   numerator, denominator = token_unpack(duration_token)
   result = [(n, denominator) 
      for n in mathtools.partition_integer_into_canonic_parts(numerator)]
   return tuple(result)
