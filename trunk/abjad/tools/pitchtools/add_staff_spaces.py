from abjad.pitch import Pitch


def add_staff_spaces(pitch, staff_spaces):
   '''Return positive integer diatonic scale degree
   corresponding to `pitch` transposed by nonnegative integer
   `staff_spaces`. ::

      abjad> pitch = Pitch(13)
      abjad> pitch.degree
      1

   ::

      abjad> pitchtools.add_staff_spaces(pitch, 0)
      1

   ::

      abjad> pitchtools.add_staff_spaces(pitch, 1)
      2

   ::

      abjad> pitchtools.add_staff_spaces(pitch, 2)
      3'''

   assert isinstance(pitch, Pitch)
   assert isinstance(staff_spaces, int)

   scale_degree = (pitch.degree + staff_spaces) % 7
   if scale_degree == 0:
      scale_degree = 7

   return scale_degree
