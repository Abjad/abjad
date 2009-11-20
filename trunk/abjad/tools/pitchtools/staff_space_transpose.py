from abjad.pitch import Pitch
from abjad.tools.pitchtools.add_staff_spaces import add_staff_spaces as \
   pitchtools_add_staff_spaces
from abjad.tools.pitchtools.diatonic_scale_degree_to_letter import \
   diatonic_scale_degree_to_letter as \
   pitchtools_diatonic_scale_degree_to_letter

def staff_space_transpose(pitch, staff_spaces, absolute_interval):
   '''Transpose `pitch` by `absolute_interval` and renotate on the
   scale degree `staff_spaces` above or below. 

   Return new pitch instance. ::

      abjad> pitch = Pitch(0)
      abjad> pitchtools.staff_space_transpose(pitch, 1, 0.5)
      Pitch('dtqf', 4)
   '''

   pitch_number = pitch.number + absolute_interval
   degree = pitchtools_add_staff_spaces(pitch, staff_spaces)
   letter = pitchtools_diatonic_scale_degree_to_letter(degree)
   return Pitch(pitch_number, letter)
