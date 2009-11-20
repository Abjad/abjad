#from abjad.accidental import Accidental
#from abjad.tools.pitchtools.letter_to_pc import letter_to_pc as \
#   pitchtools_letter_to_pc
#
#
#def letter_pitch_number_to_nearest_accidental_string(letter, number):
#   r'''Return accidental string such that `letter` followed by accidental
#   string equals pitch `number`. ::
#
#      abjad> pitchtools.letter_pitch_number_to_nearest_accidental_string('c', 10)
#      'ff'
#      abjad> pitchtools.letter_pitch_number_to_nearest_accidental_string('c', 10.5)
#      'tqf'
#      abjad> pitchtools.letter_pitch_number_to_nearest_accidental_string('c', 11)
#      'f'
#      abjad> pitchtools.letter_pitch_number_to_nearest_accidental_string('c', 11.5)
#      'qf'
#      abjad> pitchtools.letter_pitch_number_to_nearest_accidental_string('c', 12)
#      ''
#      abjad> pitchtools.letter_pitch_number_to_nearest_accidental_string('c', 12.5)
#      'qs'
#      abjad> pitchtools.letter_pitch_number_to_nearest_accidental_string('c', 13)
#      's'
#      abjad> pitchtools.letter_pitch_number_to_nearest_accidental_string('c', 13.5)
#      'tqs'
#      abjad> pitchtools.letter_pitch_number_to_nearest_accidental_string('c', 14)
#      'ss'
#   '''
#
#   givenPC = pitchtools_letter_to_pc(letter)
#   adjustment = number - givenPC
#   if adjustment % 12 > 6:
#      adjustment %= -12
#   else:
#      adjustment %= 12
#   return Accidental.adjustmentToAccidentalString[adjustment]
