from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch


def make_named_pitches_from_pitch_tokens(pitch_tokens):
   '''.. versionadded:: 1.1.2

   Construct pitches from `pitch_tokens`.::

      abjad> pitchtools.make_named_pitches_from_pitch_tokens([0, 2, 4, 5, 7, 9])
      [NamedPitch(c, 4), NamedPitch(d, 4), NamedPitch(e, 4), NamedPitch(f, 4), NamedPitch(g, 4), NamedPitch(a, 4)]

   ::

      abjad> pitchtools.make_named_pitches_from_pitch_tokens([('cs', 4), ('gs', 4), ('as', 4)])
      [NamedPitch(cs, 4), NamedPitch(gs, 4), NamedPitch(as, 4)]

   .. versionchanged:: 1.1.2
      renamed ``construct.pitches( )`` to
      ``pitchtools.make_named_pitches_from_pitch_tokens( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.make_pitches( )`` to
      ``pitchtools.make_named_pitches_from_pitch_tokens( )``.
   '''

   return [NamedPitch(pitch_token) for pitch_token in pitch_tokens]
