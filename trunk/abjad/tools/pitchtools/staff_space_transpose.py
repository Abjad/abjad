from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch
from abjad.tools.pitchtools.diatonic_scale_degree_to_letter import \
   diatonic_scale_degree_to_letter


def staff_space_transpose(pitch, staff_spaces, absolute_interval):
   '''Transpose `pitch` by `absolute_interval` and renotate on the
   scale degree `staff_spaces` above or below. 

   Return new pitch instance. ::

      abjad> pitch = NamedPitch(0)
      abjad> pitchtools.staff_space_transpose(pitch, 1, 0.5)
      NamedPitch('dtqf', 4)
   '''

   pitch_number = pitch.number + absolute_interval
   diatonic_scale_degree = pitch.degree + staff_spaces
   letter = diatonic_scale_degree_to_letter(diatonic_scale_degree)
   return NamedPitch(pitch_number, letter)
