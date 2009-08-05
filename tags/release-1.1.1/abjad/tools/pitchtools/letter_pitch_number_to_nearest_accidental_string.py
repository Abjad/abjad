from abjad.accidental import Accidental
from abjad.tools.pitchtools.letter_to_pc import letter_to_pc as \
   pitchtools_letter_to_pc


def letter_pitch_number_to_nearest_accidental_string(letter, number):
   givenPC = pitchtools_letter_to_pc(letter)
   adjustment = number - givenPC
   if adjustment % 12 > 6:
      adjustment %= -12
   else:
      adjustment %= 12
   return Accidental.adjustmentToAccidentalString[adjustment]
