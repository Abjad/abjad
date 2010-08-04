from abjad.tools.pitchtools.is_pitch_token import is_pitch_token


def is_pitch_token_collection(pitch_tokens):
   '''True when iterable `pitch_tokens` all have the form of an
   Abjad pitch token. ::

      abjad> pitchtools.is_pitch_token_collection([('c', 4), ('d', 4), NamedPitch('e', 4)])
      True
      abjad> pitchtools.is_pitch_token_collection([0, 2, 4])
      True

   Otherwise false. ::

      abjad> pitchtools.is_pitch_token_collection(['foo', 'bar'])
      False
   '''

   if isinstance(pitch_tokens, (list, tuple, set)):
      if all([is_pitch_token(x) for x in pitch_tokens]):
         return True
   return False
