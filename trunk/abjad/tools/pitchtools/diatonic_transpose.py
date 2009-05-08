from abjad.pitch.pitch import Pitch
from abjad.tools.pitchtools.diatonic_interval_to_staff_spaces import \
   diatonic_interval_to_staff_spaces as \
   pitchtools_diatonic_interval_to_staff_spaces
from abjad.tools.pitchtools.add_staff_spaces import add_staff_spaces as \
   pitchtools_add_staff_spaces
from abjad.tools.pitchtools.diatonic_scale_degree_to_letter import \
   diatonic_scale_degree_to_letter as \
   pitchtools_diatonic_scale_degree_to_letter
from abjad.tools.pitchtools.diatonic_interval_to_absolute_interval import \
   diatonic_interval_to_absolute_interval as \
   pitchtools_diatonic_interval_to_absolute_interval
from abjad.tools.pitchtools.letter_pitch_number_to_nearest_accidental_string \
   import letter_pitch_number_to_nearest_accidental_string as \
   pitchtools_letter_pitch_number_to_nearest_accidental_string
from abjad.tools.pitchtools.letter_pitch_number_to_octave import \
   letter_pitch_number_to_octave as pitchtools_letter_pitch_number_to_octave


#def diatonicTranspose(self, diatonicInterval):
def diatonic_transpose(pitch, diatonicInterval):
   quality, interval = diatonicInterval.split( )
   #staffSpaces = self.tools.diatonicIntervalToStaffSpaces[interval]
   staffSpaces = pitchtools_diatonic_interval_to_staff_spaces(interval)
   #degree = self.tools.addStaffSpaces(staffSpaces)
   degree = pitchtools_add_staff_spaces(pitch, staffSpaces)
   #letter = self.tools.diatonicScaleDegreeToLetter[degree]
   letter = pitchtools_diatonic_scale_degree_to_letter(degree)
   #pitchNumber = self.number + \
   #   self.tools.diatonicIntervalToAbsoluteInterval[diatonicInterval]
   pitchNumber = pitch.number + \
      pitchtools_diatonic_interval_to_absolute_interval(diatonicInterval)
   #accidentalString = self.tools.letterPitchNumberToNearestAccidentalString(
   #   letter, pitchNumber)
   accidentalString = \
      pitchtools_letter_pitch_number_to_nearest_accidental_string(
      letter, pitchNumber)
   pitchName = letter + accidentalString
   #octave = self.tools.letterPitchNumberToOctave(letter, pitchNumber)
   octave = pitchtools_letter_pitch_number_to_octave(letter, pitchNumber)
   return Pitch(pitchName, octave)
