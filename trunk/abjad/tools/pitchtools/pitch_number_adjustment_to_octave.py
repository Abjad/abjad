import math


def pitch_number_adjustment_to_octave(pitch_number, accidental_adjustment):
   '''Return integer octave number of `pitch_number` when spelled
   with unspecified pitch letter followed by numeric
   `accidental_adjustment`. ::


      abjad> pitchtools.pitch_number_accidental_adjustment_to_octave(12, 0)
      5
      abjad> pitchtools.pitch_number_accidental_adjustment_to_octave(12, -1)
      5
      abjad> pitchtools.pitch_number_accidental_adjustment_to_octave(12, -2)
      5
      abjad> pitchtools.pitch_number_accidental_adjustment_to_octave(12, 1)
      4
      abjad> pitchtools.pitch_number_accidental_adjustment_to_octave(12, 2)
      4
   '''

   return int(math.floor((pitch_number - accidental_adjustment) / 12)) + 4
