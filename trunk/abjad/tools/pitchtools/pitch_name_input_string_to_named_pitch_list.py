from abjad.tools.pitchtools.pitch_name_to_named_pitch import pitch_name_to_named_pitch


def pitch_name_input_string_to_named_pitch_list(pitch_string):
   '''.. versionadded:: 1.1.2

   Convert whitespace-delimited string of LilyPond-style pitch names
   to list of zero or more Abjad pitch instances. ::

      abjad> pitchtools.pitch_name_to_named_pitch("cs, cs cs' cs''")
      [NamedPitch(c, 2), NamedPitch(c, 3), NamedPitch(c, 4), NamedPitch(c, 5)]

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_string_to_pitches( )`` to
      ``pitchtools.pitch_name_input_string_to_named_pitch_list( )``.
   '''

   pitches = [ ]
   pitch_strings = pitch_string.split( )
   for pitch_string in pitch_strings:
      pitch = pitch_name_to_named_pitch(pitch_string)
      pitches.append(pitch)

   return pitches
