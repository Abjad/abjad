def pitch_name_to_named_pitch(pitch_string):
   '''.. versionadded:: 1.1.2

   Convert LilyPond-style `pitch_string` to Ajbad pitch instance. ::

      abjad> pitchtools.pitch_name_to_named_pitch("css''")
      NamedPitch(css, 5)

   Equivalent to ``Pitch(pitch_string)``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_string_to_pitch( )`` to
      ``pitchtools.pitch_name_to_named_pitch( )``.
   '''

   from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch

   pitch = NamedPitch(pitch_string)
   return pitch
