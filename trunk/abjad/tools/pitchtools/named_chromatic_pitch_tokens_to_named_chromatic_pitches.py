from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch


def named_chromatic_pitch_tokens_to_named_chromatic_pitches(pitch_tokens):
   '''.. versionadded:: 1.1.2

   Construct pitches from `pitch_tokens`.::

      abjad> pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([0, 2, 4, 5, 7, 9])
      [NamedPitch(c, 4), NamedPitch(d, 4), NamedPitch(e, 4), NamedPitch(f, 4), NamedPitch(g, 4), NamedPitch(a, 4)]

   ::

      abjad> pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([('cs', 4), ('gs', 4), ('as', 4)])
      [NamedPitch(cs, 4), NamedPitch(gs, 4), NamedPitch(as, 4)]

   .. versionchanged:: 1.1.2
      renamed ``construct.pitches( )`` to
      ``pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.make_pitches( )`` to
      ``pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.make_named_pitches_from_pitch_tokens( )`` to
      ``pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches( )``.
   '''

   return [NamedPitch(pitch_token) for pitch_token in pitch_tokens]
