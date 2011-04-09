from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch


def named_chromatic_pitch_tokens_to_named_chromatic_pitches(pitch_tokens):
   '''.. versionadded:: 1.1.2

   Convert named chromatic `pitch_tokens` to named chromatic pitches::

      abjad> pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([0, 2, ('ef', 4)])
      [NamedChromaticPitch(c, 4), NamedChromaticPitch(d, 4), NamedChromaticPitch(ef, 4)]

   Return list of zero or more named chromatic pitches.
   '''

   return [NamedChromaticPitch(pitch_token) for pitch_token in pitch_tokens]
