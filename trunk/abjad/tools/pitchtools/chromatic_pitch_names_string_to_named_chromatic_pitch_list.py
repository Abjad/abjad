from abjad.tools.pitchtools.NamedChromaticPitch import NamedChromaticPitch


def chromatic_pitch_names_string_to_named_chromatic_pitch_list(chromatic_pitch_names_string):
   '''.. versionadded:: 1.1.2

   Change `chromatic_pitch_names_string` to named chromatic pitch list::

      abjad> pitchtools.chromatic_pitch_names_string_to_named_chromatic_pitch_list("cs, cs cs' cs''")
      [NamedChromaticPitch(c, 2), NamedChromaticPitch(c, 3), NamedChromaticPitch(c, 4), NamedChromaticPitch(c, 5)]

   Return list of named chromatic pitches.
   '''

   pitches = [ ]
   pitch_strings = chromatic_pitch_names_string.split( )
   for pitch_string in pitch_strings:
      pitch = NamedChromaticPitch(pitch_string)
      pitches.append(pitch)

   return pitches
