from abjad.tools.pitchtools.pitch_class_number_to_pitch_name_with_flats import pitch_class_number_to_pitch_name_with_flats as pitchtools_pitch_class_number_to_pitch_name_with_flats
from abjad.tools.pitchtools.pitch_class_number_to_pitch_name_with_flats_flats import pitch_class_number_to_pitch_name_with_flats_flats as pitchtools_pitch_class_number_to_pitch_name_with_flats_flats
from abjad.tools.pitchtools.pitch_class_number_to_pitch_name_with_flats_sharps import pitch_class_number_to_pitch_name_with_flats_sharps as pitchtools_pitch_class_number_to_pitch_name_with_flats_sharps
import math


def pitch_number_to_pitch_letter_alphabetic_accidental_string_and_octave_number_triple(number, spelling = 'mixed'):
   '''.. versionadded: 1.1.1

   Convert pitch `number` and optional `spelling` to unique triple
   of letter, accidental and octave. ::

      abjad> pitchtools.pitch_number_to_pitch_letter_alphabetic_accidental_string_and_octave_number_triple(13, 'sharps')

   .. todo: Write tests.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.number_to_letter_accidental_octave( )`` to
      ``pitchtools.pitch_number_to_pitch_letter_alphabetic_accidental_string_and_octave_number_triple( )``.
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
      pitch_name = pitchtools_pitch_class_number_to_pitch_name_with_flats(pc)
   elif spelling == 'sharps':
      pitch_name = pitchtools_pitch_class_number_to_pitch_name_with_flats_sharps(pc)
   elif spelling == 'flats':
      pitch_name = pitchtools_pitch_class_number_to_pitch_name_with_flats_flats(pc)
   else:
      raise ValueError('unknown accidental spelling.')

   ## disassemble pitch name into letter and accidental
   letter = pitch_name[0]
   accidental = pitch_name[1:]

   ## find octave
   octave = int(math.floor(number / 12)) + 4

   ## return uninque letter, accidental, octave triple
   return letter, accidental, octave
