from abjad.pitch import Pitch
from abjad.tools.pitchtools.DiatonicInterval import DiatonicInterval
from abjad.tools.pitchtools.add_staff_spaces import add_staff_spaces as \
   pitchtools_add_staff_spaces
from abjad.tools.pitchtools.diatonic_interval_string_to_diatonic_interval_number import diatonic_interval_string_to_diatonic_interval_number
from abjad.tools.pitchtools.diatonic_scale_degree_to_letter import \
   diatonic_scale_degree_to_letter as \
   pitchtools_diatonic_scale_degree_to_letter
from abjad.tools.pitchtools.letter_pitch_number_to_nearest_accidental_string \
   import letter_pitch_number_to_nearest_accidental_string as \
   pitchtools_letter_pitch_number_to_nearest_accidental_string
from abjad.tools.pitchtools.letter_pitch_number_to_octave import \
   letter_pitch_number_to_octave as pitchtools_letter_pitch_number_to_octave


def diatonic_transpose(pitch, diatonic_interval):
   '''Return new pitch equal to `pitch` transposed up by
   `diatonic_interval` string. ::

      abjad> pitchtools.diatonic_transpose(Pitch('c', 4), 'perfect unison')
      Pitch(c, 4)
      abjad> pitchtools.diatonic_transpose(Pitch('c', 4), 'minor second')
      Pitch(df, 4)
      abjad> pitchtools.diatonic_transpose(Pitch('c', 4), 'major second')
      Pitch(d, 4)
      abjad> pitchtools.diatonic_transpose(Pitch('c', 4), 'minor third')
      Pitch(ef, 4)

   Down-transposition is not possible with this function.
   '''

   quality_string, diatonic_interval_string = diatonic_interval.split( )
   diatonic_interval_number = \
      diatonic_interval_string_to_diatonic_interval_number(
      diatonic_interval_string)
   di = DiatonicInterval(
      quality_string, diatonic_interval_number)
   degree = pitchtools_add_staff_spaces(pitch, di.staff_spaces)
   letter = pitchtools_diatonic_scale_degree_to_letter(degree)
   chromatic_pitch_number = pitch.number + di.semitones
   accidental_string = \
      pitchtools_letter_pitch_number_to_nearest_accidental_string(
      letter, chromatic_pitch_number)
   pitch_name = letter + accidental_string
   octave = pitchtools_letter_pitch_number_to_octave(
      letter, chromatic_pitch_number)
   return Pitch(pitch_name, octave)
