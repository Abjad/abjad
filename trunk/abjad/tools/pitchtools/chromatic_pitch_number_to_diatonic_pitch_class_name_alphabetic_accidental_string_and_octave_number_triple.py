from abjad.tools.pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name import chromatic_pitch_class_number_to_chromatic_pitch_class_name
from abjad.tools.pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats import chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats
from abjad.tools.pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps import chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps
import math


def chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_string_and_octave_number_triple(number, spelling = 'mixed'):
   '''.. versionadded: 1.1.1

   Convert pitch `number` and optional `spelling` to unique triple
   of letter, accidental and octave. ::

      abjad> pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_string_and_octave_number_triple(13, 'sharps')

   .. todo: Write tests.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.number_to_letter_accidental_octave( )`` to
      ``pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_string_and_octave_number_triple( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_number_to_pitch_letter_alphabetic_accidental_string_and_octave_number_triple( )`` to
      ``pitchtools.chromatic_pitch_number_to_diatonic_pitch_class_name_alphabetic_accidental_string_and_octave_number_triple( )``.
   '''

   ## check input
   if not isinstance(number, (int, long, float)):
      raise TypeError

   if not isinstance(spelling, str):
      raise TypeError

   if not spelling in ('mixed', 'flats', 'sharps'):
      raise ValueError

   ## find pc
   pc = number % 12

   ## find pitch name from pc according to spelling
   if spelling == 'mixed':
      pitch_name = chromatic_pitch_class_number_to_chromatic_pitch_class_name(pc)
   elif spelling == 'sharps':
      pitch_name = chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps(pc)
   elif spelling == 'flats':
      pitch_name = chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats(pc)
   else:
      raise ValueError('unknown accidental spelling.')

   ## disassemble pitch name into letter and accidental
   letter = pitch_name[0]
   accidental = pitch_name[1:]

   ## find octave
   octave = int(math.floor(number / 12)) + 4

   ## return uninque letter, accidental, octave triple
   return letter, accidental, octave
