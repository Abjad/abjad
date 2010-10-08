from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch


def named_chromatic_pitch_tokens_to_named_chromatic_pitches(pitch_tokens):
   '''.. versionadded:: 1.1.2

   Construct pitches from `pitch_tokens`.::

      abjad> pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([0, 2, 4, 5, 7, 9])
      [NamedChromaticPitch(c, 4), NamedChromaticPitch(d, 4), NamedChromaticPitch(e, 4), NamedChromaticPitch(f, 4), NamedChromaticPitch(g, 4), NamedChromaticPitch(a, 4)]

   ::

      abjad> pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([('cs', 4), ('gs', 4), ('as', 4)])
      [NamedChromaticPitch(cs, 4), NamedChromaticPitch(gs, 4), NamedChromaticPitch(as, 4)]

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

   return [NamedChromaticPitch(pitch_token) for pitch_token in pitch_tokens]
