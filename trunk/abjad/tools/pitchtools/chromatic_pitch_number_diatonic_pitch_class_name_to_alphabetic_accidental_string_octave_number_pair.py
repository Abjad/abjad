from abjad.tools.pitchtools.Accidental import Accidental
from abjad.tools.pitchtools.diatonic_pitch_class_name_to_chromatic_pitch_class_number import diatonic_pitch_class_name_to_chromatic_pitch_class_number as pitchtools_diatonic_pitch_class_name_to_chromatic_pitch_class_number
from abjad.tools.pitchtools.transpose_chromatic_pitch_class_number_by_octaves_to_nearest_neighbor_of_chromatic_pitch_number import transpose_chromatic_pitch_class_number_by_octaves_to_nearest_neighbor_of_chromatic_pitch_number as pitchtools_transpose_chromatic_pitch_class_number_by_octaves_to_nearest_neighbor_of_chromatic_pitch_number
from abjad.tools.pitchtools.chromatic_pitch_number_and_accidental_semitones_to_octave_number import chromatic_pitch_number_and_accidental_semitones_to_octave_number


def chromatic_pitch_number_diatonic_pitch_class_name_to_alphabetic_accidental_string_octave_number_pair(number, letter):
   '''.. versionadded:: 1.1.1

   Return accidental, octave pair necessary to notate pitch `number`
   spelled starting with pitch `letter`. ::

      abjad> pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_alphabetic_accidental_string_octave_number_pair(14, 'c')
      ('ss', 5)

   ::

      abjad> pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_alphabetic_accidental_string_octave_number_pair(14, 'd')
      ('', 5)

   ::

      abjad> pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_alphabetic_accidental_string_octave_number_pair(14, 'e')
      ('ff', 5)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.number_letter_to_accidental_octave( )`` to
      ``pitchtools.chromatic_pitch_number_diatonic_pitch_class_name_to_alphabetic_accidental_string_octave_number_pair( )``.
   '''

   ## check input
   if not isinstance(number, (int, long, float)):
      raise TypeError

   if not isinstance(letter, str):
      raise TypeError

   if not letter in ['c', 'd', 'e', 'f', 'g', 'a', 'b']:
      raise ValueError
   
   ## find accidental semitones
   pc = pitchtools_diatonic_pitch_class_name_to_chromatic_pitch_class_number(letter)
   nearest_neighbor = pitchtools_transpose_chromatic_pitch_class_number_by_octaves_to_nearest_neighbor_of_chromatic_pitch_number(number, pc)
   semitones = number - nearest_neighbor
   
   ## find accidental alphabetic string
   alphabetic_string = Accidental._semitones_to_alphabetic_string[semitones]
   
   ## find octave
   octave = chromatic_pitch_number_and_accidental_semitones_to_octave_number(
      number, semitones)

   ## return unique pair of accidental string and octave
   return alphabetic_string, octave
