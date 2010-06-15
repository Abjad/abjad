from abjad.tools.durtools.duration_token_to_reduced_duration_pair import duration_token_to_reduced_duration_pair
from abjad.tools import mathtools


def duration_token_to_big_endian_list_of_assignable_duration_pairs(duration_token):
   '''Return big-endian list of note-head-assignable duration tokens
   equal to `duration_token`. ::

      abjad> duration_tokens = [(n, 16) for n in range(10, 20)]
      abjad> for duration_token in duration_tokens:
      ...     print duration_token, durtools.duration_token_to_big_endian_list_of_assignable_duration_pairs(duration_token)
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

   .. versionchanged:: 1.1.2
      renamed ``durtools.token_decompose( )`` to
      ``durtools.duration_token_to_big_endian_list_of_assignable_duration_pairs( )``.
   '''

   numerator, denominator = duration_token_to_reduced_duration_pair(duration_token)
   result = [(n, denominator) 
      for n in mathtools.partition_integer_into_canonic_parts(numerator)]
   return tuple(result)
