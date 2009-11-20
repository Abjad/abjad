#from abjad.accidental import Accidental
#from abjad.tools.pitchtools.letter_pitch_number_to_nearest_accidental_string \
#   import letter_pitch_number_to_nearest_accidental_string as \
#   pitchtools_letter_pitch_number_to_nearest_accidental_string
#from abjad.tools.pitchtools.pitch_number_to_octave import \
#   pitch_number_to_octave as pitchtools_pitch_number_to_octave
#
#
#def letter_pitch_number_to_octave(letter, pitch_number):
#   r'''Return integer octave number necessary to notate `pitch_number`
#   spelled with pitch `letter`. ::
#
#      abjad> pitchtools.letter_pitch_number_to_octave('c', 12)
#      5
#      abjad> pitchtools.letter_pitch_number_to_octave('c', 13)
#      5
#      abjad> pitchtools.letter_pitch_number_to_octave('c', 24)
#      6
#      abjad> pitchtools.letter_pitch_number_to_octave('c', 25)
#      6
#   '''
# 
#   # pitch number 12 notated as letter 'b' with accidentals
#   accidentalString = \
#      pitchtools_letter_pitch_number_to_nearest_accidental_string(
#      letter, pitch_number)
#   adjustment = Accidental.accidentalStringToAdjustment[accidentalString]
#   adjustedPitchNumber = pitch_number - adjustment
#   return pitchtools_pitch_number_to_octave(adjustedPitchNumber)
