from abjad.pitch import Pitch


def make_pitches(pitch_tokens):
   '''.. versionadded:: 1.1.2

   Construct pitches from `pitch_tokens`.::

      abjad> pitchtools.make_pitches([0, 2, 4, 5, 7, 9])
      [Pitch(c, 4), Pitch(d, 4), Pitch(e, 4), Pitch(f, 4), Pitch(g, 4), Pitch(a, 4)]

   ::

      abjad> pitchtools.make_pitches([('cs', 4), ('gs', 4), ('as', 4)])
      [Pitch(cs, 4), Pitch(gs, 4), Pitch(as, 4)]

   .. versionchanged:: 1.1.2
      renamed ``construct.pitches( )`` to
      ``pitchtools.make_pitches( )``.
   '''

   return [Pitch(pitch_token) for pitch_token in pitch_tokens]
