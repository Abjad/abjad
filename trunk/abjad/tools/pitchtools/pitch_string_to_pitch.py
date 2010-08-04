def pitch_string_to_pitch(pitch_string):
   '''.. versionadded:: 1.1.2

   Convert LilyPond-style `pitch_string` to Ajbad pitch instance. ::

      abjad> pitchtools.pitch_string_to_pitch("css''")
      NamedPitch(css, 5)

   Equivalent to ``Pitch(pitch_string)``.
   '''

   from abjad.NamedPitch import NamedPitch

   pitch = NamedPitch(pitch_string)
   return pitch
