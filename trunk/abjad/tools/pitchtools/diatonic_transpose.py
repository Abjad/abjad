from abjad.pitch import Pitch
from abjad.tools.pitchtools.DiatonicInterval import DiatonicInterval
from abjad.tools.pitchtools.diatonic_scale_degree_to_letter import \
   diatonic_scale_degree_to_letter


def diatonic_transpose(pitch, diatonic_interval):
   '''Return new pitch equal to `pitch` transposed up or down by
   `diatonic_interval` string. ::

      abjad> diatonic_interval = pitchtools.DiatonicInterval('perfect', 1)
      abjad> pitchtools.diatonic_transpose(Pitch('c', 4), diatonic_interval)
      Pitch(c, 4)

   ::

      abjad> diatonic_interval = pitchtools.DiatonicInterval('minor', 2)
      abjad> pitchtools.diatonic_transpose(Pitch('c', 4), 'minor second')
      Pitch(df, 4)

   ::

      abjad> diatonic_interval = pitchtools.DiatonicInterval('minor', -2)
      abjad> pitchtools.diatonic_transpose(pitch, diatonic_interval)
      Pitch(b, 3)

   ::

      abjad> diatonic_interval = pitchtools.DiatonicInterval('major', 2)
      abjad> pitchtools.diatonic_transpose(Pitch('c', 4), 'major second')
      Pitch(d, 4)

   ::

      abjad> diatonic_interval = pitchtools.DiatonicInterval('major', -2)
      abjad> pitchtools.diatonic_transpose(pitch, diatonic_interval)
      Pitch(bf, 3)
   '''

   chromatic_pitch_number = pitch.number + diatonic_interval.semitones
   diatonic_scale_degree = pitch.degree + diatonic_interval.staff_spaces
   letter = diatonic_scale_degree_to_letter(diatonic_scale_degree)
   return Pitch(chromatic_pitch_number, letter)
