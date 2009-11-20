from abjad.pitch import Pitch
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

   quality, interval = diatonic_interval.split( )
   staffSpaces = pitchtools_diatonic_interval_to_staff_spaces(interval)
   degree = pitchtools_add_staff_spaces(pitch, staffSpaces)
   letter = pitchtools_diatonic_scale_degree_to_letter(degree)
   pitchNumber = pitch.number + \
      pitchtools_diatonic_interval_to_absolute_interval(diatonic_interval)
   accidentalString = \
      pitchtools_letter_pitch_number_to_nearest_accidental_string(
      letter, pitchNumber)
   pitchName = letter + accidentalString
   octave = pitchtools_letter_pitch_number_to_octave(letter, pitchNumber)
   return Pitch(pitchName, octave)
