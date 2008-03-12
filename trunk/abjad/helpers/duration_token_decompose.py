from abjad.helpers.duration_token_unpack import _duration_token_unpack
from abjad.helpers.integer_decompose import _integer_decompose

def _duration_token_decompose(duration_token):
   '''Return big-endian list of notehead-assignable duration tokens.

      >>> duration_tokens = [(n, 16) for n in range(10, 20)]
      >>> for duration_token in duration_tokens:
      ...     print duration_token, _duration_token_decompose(duration_token)
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
      (19, 16) ((16, 16), (3, 16))
   '''

   numerator, denominator = _duration_token_unpack(duration_token)
   result = [(n, denominator) for n in _integer_decompose(numerator)]
   return tuple(result)
