from abjad.tools.pitchtools.pitch_string_to_pitch import \
   pitch_string_to_pitch


def pitch_string_to_pitches(pitch_string):
   '''.. versionadded:: 1.1.2

   Convert whitespace-delimited string of LilyPond-style pitch names
   to list of zero or more Abjad pitch instances. ::

      abjad> pitchtools.pitch_string_to_pitch("cs, cs cs' cs''")
      [Pitch(c, 2), Pitch(c, 3), Pitch(c, 4), Pitch(c, 5)]
   '''

   pitches = [ ]
   pitch_strings = pitch_string.split( )
   for pitch_string in pitch_strings:
      pitch = pitch_string_to_pitch(pitch_string)
      pitches.append(pitch)

   return pitches
