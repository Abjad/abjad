from abjad.pitch import Pitch
from abjad.tools.pitchtools.DiatonicInterval import DiatonicInterval
from abjad.tools.pitchtools.add_staff_spaces import add_staff_spaces as \
   pitchtools_add_staff_spaces
from abjad.tools.pitchtools.diatonic_scale_degree_to_letter import \
   diatonic_scale_degree_to_letter as \
   pitchtools_diatonic_scale_degree_to_letter


def diatonic_transpose(pitch, diatonic_interval):
   '''Return new pitch equal to `pitch` transposed up by
   `diatonic_interval` string. ::

      abjad> diatonic_interval = pitchtools.DiatonicInterval('perfect', 1)
      abjad> pitchtools.diatonic_transpose(Pitch('c', 4), diatonic_interval)
      Pitch(c, 4)

   ::

      abjad> diatonic_interval = pitchtools.DiatonicInterval('minor', 2)
      abjad> pitchtools.diatonic_transpose(Pitch('c', 4), 'minor second')
      Pitch(df, 4)

   ::

      abjad> diatonic_interval = pitchtools.DiatonicInterval('major', 2)
      abjad> pitchtools.diatonic_transpose(Pitch('c', 4), 'major second')
      Pitch(d, 4)

   ::

      abjad> diatonic_interval = pitchtools.DiatonicInterval('minor', 3)
      abjad> pitchtools.diatonic_transpose(Pitch('c', 4), 'minor third')
      Pitch(ef, 4)

   Down-transposition is not possible with this function.
   '''

   degree = pitchtools_add_staff_spaces(pitch, diatonic_interval.staff_spaces)
   letter = pitchtools_diatonic_scale_degree_to_letter(degree)
   chromatic_pitch_number = pitch.number + diatonic_interval.semitones
   return Pitch(chromatic_pitch_number, letter)
