from abjad.tools.pitchtools.is_token import is_token


def is_token_collection(tokens):
   '''True when iterable `tokens` all have the form of an
   Abjad pitch token. ::

      abjad> pitchtools.is_token_collection([('c', 4), ('d', 4), Pitch('e', 4)])
      True
      abjad> pitchtools.is_token_collection([0, 2, 4])
      True

   Otherwise false. ::

      abjad> pitchtools.is_token_collection(['foo', 'bar'])
      False
   '''

   if isinstance(tokens, (list, tuple, set)):
      if all([is_token(x) for x in tokens]):
         return True
   return False
