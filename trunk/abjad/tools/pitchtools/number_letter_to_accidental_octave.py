from abjad.tools.pitchtools.Accidental import Accidental
from abjad.tools.pitchtools.letter_to_pc import \
   letter_to_pc as pitchtools_letter_to_pc
from abjad.tools.pitchtools.nearest_neighbor import \
   nearest_neighbor as pitchtools_nearest_neighbor
from abjad.tools.pitchtools.pitch_number_adjustment_to_octave import \
   pitch_number_adjustment_to_octave as \
   pitchtools_pitch_number_adjustment_to_octave


def number_letter_to_accidental_octave(number, letter):
   '''.. versionadded:: 1.1.1

   Return accidental, octave pair necessary to notate pitch `number`
   spelled starting with pitch `letter`. ::

      abjad> pitchtools.number_letter_to_accidental_octave(14, 'c')
      ('ss', 5)

   ::

      abjad> pitchtools.number_letter_to_accidental_octave(14, 'd')
      ('', 5)

   ::

      abjad> pitchtools.number_letter_to_accidental_octave(14, 'e')
      ('ff', 5)
   '''

   ## check input
   if not isinstance(number, (int, long, float)):
      raise TypeError

   if not isinstance(letter, str):
      raise TypeError

   if not letter in ['c', 'd', 'e', 'f', 'g', 'a', 'b']:
      raise ValueError
   
   ## find accidental adjustment
   pc = pitchtools_letter_to_pc(letter)
   nearest_neighbor = pitchtools_nearest_neighbor(number, pc)
   adjustment = number - nearest_neighbor
   
   ## find accidental string
   accidental_string = Accidental.adjustmentToAccidentalString[adjustment]
   
   ## find octave
   octave = pitchtools_pitch_number_adjustment_to_octave(number, adjustment)

   ## return unique pair of accidental string and octave
   return accidental_string, octave
