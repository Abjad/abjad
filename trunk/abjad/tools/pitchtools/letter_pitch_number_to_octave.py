from abjad.accidental import Accidental
from abjad.tools.pitchtools.letter_pitch_number_to_nearest_accidental_string \
   import letter_pitch_number_to_nearest_accidental_string as \
   pitchtools_letter_pitch_number_to_nearest_accidental_string
from abjad.tools.pitchtools.pitch_number_to_octave import \
   pitch_number_to_octave as pitchtools_pitch_number_to_octave


def letter_pitch_number_to_octave(letter, pitchNumber):
   # pitch number 12 notated as letter 'b' with accidentals
   accidentalString = \
      pitchtools_letter_pitch_number_to_nearest_accidental_string(
      letter, pitchNumber)
   adjustment = Accidental.accidentalStringToAdjustment[accidentalString]
   adjustedPitchNumber = pitchNumber - adjustment
   return pitchtools_pitch_number_to_octave(adjustedPitchNumber)
