import math


def chromatic_pitch_number_and_accidental_semitones_to_octave_number(
   pitch_number, accidental_semitones):
   '''Return integer octave number of `pitch_number` when spelled
   with unspecified pitch letter followed by numeric
   `accidental_semitones`. ::


      abjad> pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number(12, 0)
      5
      abjad> pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number(12, -1)
      5
      abjad> pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number(12, -2)
      5
      abjad> pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number(12, 1)
      4
      abjad> pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number(12, 2)
      4

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_number_and_accidental_semitones_to_octave( )`` to
      ``pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_number_and_accidental_semitones_to_octave_number( )`` to
      ``pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number( )``.
   '''

   return int(math.floor((pitch_number - accidental_semitones) / 12)) + 4
