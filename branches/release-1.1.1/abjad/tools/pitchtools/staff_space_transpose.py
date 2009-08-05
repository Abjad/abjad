from abjad.pitch import Pitch
from abjad.tools.pitchtools.add_staff_spaces import add_staff_spaces as \
   pitchtools_add_staff_spaces
from abjad.tools.pitchtools.diatonic_scale_degree_to_letter import \
   diatonic_scale_degree_to_letter as \
   pitchtools_diatonic_scale_degree_to_letter

def staff_space_transpose(pitch, staffSpaces, absoluteInterval):
   '''p.staffSpaceTranspose(-1, 0.5)'''
   pitchNumber = pitch.number + absoluteInterval
   #degree = self.tools.addStaffSpaces(staffSpaces)
   degree = pitchtools_add_staff_spaces(pitch, staffSpaces)
   #letter = self.tools.diatonicScaleDegreeToLetter[degree]
   letter = pitchtools_diatonic_scale_degree_to_letter(degree)
   return Pitch(pitchNumber, letter)
