from abjad.tools.pitchtools.NamedChromaticPitch import NamedChromaticPitch


def chromatic_pitch_names_string_to_named_chromatic_pitch_list(pitch_string):
   '''.. versionadded:: 1.1.2

   Convert whitespace-delimited string of LilyPond-style pitch names
   to list of zero or more Abjad pitch instances::

      abjad> pitchtools.chromatic_pitch_names_string_to_named_chromatic_pitch_list("cs, cs cs' cs''")
      [NamedChromaticPitch(c, 2), NamedChromaticPitch(c, 3), NamedChromaticPitch(c, 4), NamedChromaticPitch(c, 5)]

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_string_to_pitches( )`` to
      ``pitchtools.chromatic_pitch_names_string_to_named_chromatic_pitch_list( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_name_input_string_to_named_pitch_list( )`` to
      ``pitchtools.chromatic_pitch_names_string_to_named_chromatic_pitch_list( )``.
   '''

   pitches = [ ]
   pitch_strings = pitch_string.split( )
   for pitch_string in pitch_strings:
      pitch = NamedChromaticPitch(pitch_string)
      pitches.append(pitch)

   return pitches
