from abjad.tools.pitchtools.add_staff_spaces import add_staff_spaces
from abjad.tools.pitchtools.diatonic_scale_degree_to_letter import \
   diatonic_scale_degree_to_letter


def transpose_by_diatonic_interval(expr, diatonic_interval):
   '''.. versionadded:: 1.1.2

   Transpose all pitch carriers in `expr` by `diatonic_interval`. ::

      abjad>

   .. todo:: FINISH IMPLEMENTATION.
   '''

   if not isinstance(diatonic_interval, DiatonicInterval):
      raise TypeError('must be diatonic interval.')

   

def _transpose_pitch_by_diatonic_interval(pitch, diatonic_interval):

   if not isinstance(pitch, Pitch):
      raise TypeError('must be pitch.')

   chromatic_pitch_number = pitch.number + diatonic_interval.semitones
   diatonic_scale_degree = add_staff_spaces(
      pitch, diatonic_interval.staff_spaces)
   letter = diatonic_scale_degree_to_letter(diatonic_scale_degree)
   return Pitch(chromatic_pitch_number, letter)
