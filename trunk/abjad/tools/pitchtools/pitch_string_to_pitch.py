def pitch_string_to_pitch(pitch_string):
   '''.. versionadded:: 1.1.2

   Convert LilyPond-style `pitch_string` to Ajbad pitch instance. ::

      abjad> pitchtools.pitch_string_to_pitch("css''")
      Pitch(css, 5)

   Equivalent to ``Pitch(pitch_string)``.
   '''

   from abjad.pitch import Pitch

   pitch = Pitch(pitch_string)
   return pitch
