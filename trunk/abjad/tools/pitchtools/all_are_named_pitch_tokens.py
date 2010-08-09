from abjad.tools.pitchtools.is_named_pitch_token import is_named_pitch_token


def all_are_named_pitch_tokens(pitch_tokens):
   '''True when iterable `pitch_tokens` all have the form of an
   Abjad pitch token. ::

      abjad> pitchtools.all_are_named_pitch_tokens([('c', 4), ('d', 4), NamedPitch('e', 4)])
      True
      abjad> pitchtools.all_are_named_pitch_tokens([0, 2, 4])
      True

   Otherwise false. ::

      abjad> pitchtools.all_are_named_pitch_tokens(['foo', 'bar'])
      False

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.is_pitch_token_collection( )`` to
      ``pitchtools.all_are_named_pitch_tokens( )``.
   '''

   if isinstance(pitch_tokens, (list, tuple, set)):
      if all([is_named_pitch_token(x) for x in pitch_tokens]):
         return True
   return False
