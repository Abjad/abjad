import math


def pitch_number_to_octave(pitch_number):
   '''Return integer octave number corresponding to `pitch_number`.

   ::

      abjad> pitchtools.pitch_number_to_octave(-12)
      3
      abjad> pitchtools.pitch_number_to_octave(-11)
      3
      abjad> pitchtools.pitch_number_to_octave(0)
      4
      abjad> pitchtools.pitch_number_to_octave(1)
      4
      abjad> pitchtools.pitch_number_to_octave(12)
      5
      abjad> pitchtools.pitch_number_to_octave(13)
      5
   '''

   return int(math.floor(pitch_number / 12)) + 4
