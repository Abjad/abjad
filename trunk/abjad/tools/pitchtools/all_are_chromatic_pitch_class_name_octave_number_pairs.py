from abjad.tools.pitchtools.is_named_chromatic_pitch_token import is_named_chromatic_pitch_token


def all_are_chromatic_pitch_class_name_octave_number_pairs(pitch_tokens):
   '''True when iterable `pitch_tokens` all have the form of an
   Abjad pitch token. ::

      abjad> pitchtools.all_are_chromatic_pitch_class_name_octave_number_pairs([('c', 4), ('d', 4), NamedChromaticPitch('e', 4)])
      True
      abjad> pitchtools.all_are_chromatic_pitch_class_name_octave_number_pairs([0, 2, 4])
      True

   Otherwise false. ::

      abjad> pitchtools.all_are_chromatic_pitch_class_name_octave_number_pairs(['foo', 'bar'])
      False

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.is_pitch_token_collection( )`` to
      ``pitchtools.all_are_chromatic_pitch_class_name_octave_number_pairs( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.all_are_named_pitch_tokens( )`` to
      ``pitchtools.all_are_chromatic_pitch_class_name_octave_number_pairs( )``.
   '''

   if isinstance(pitch_tokens, (list, tuple, set)):
      if all([is_named_chromatic_pitch_token(x) for x in pitch_tokens]):
         return True
   return False
