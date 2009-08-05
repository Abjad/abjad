from abjad.tools.pitchtools.pc_to_pitch_name import \
   pc_to_pitch_name as pitchtools_pc_to_pitch_name
from abjad.tools.pitchtools.pc_to_pitch_name_flats import \
   pc_to_pitch_name_flats as pitchtools_pc_to_pitch_name_flats
from abjad.tools.pitchtools.pc_to_pitch_name_sharps import \
   pc_to_pitch_name_sharps as pitchtools_pc_to_pitch_name_sharps
import math


def number_to_letter_accidental_octave(number, spelling = 'mixed'):
   '''.. versionadded: 1.1.1

   Convert pitch `number` and optional `spelling` to unique triple
   of letter, accidental and octave. ::

      abjad> pitchtools.number_to_letter_accidental_octave(13, 'sharps')

   .. todo: Write tests.
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
      pitch_name = pitchtools_pc_to_pitch_name(pc)
   elif spelling == 'sharps':
      pitch_name = pitchtools_pc_to_pitch_name_sharps(pc)
   elif spelling == 'flats':
      pitch_name = pitchtools_pc_to_pitch_name_flats(pc)
   else:
      raise ValueError('unknown accidental spelling.')

   ## disassemble pitch name into letter and accidental
   letter = pitch_name[0]
   accidental = pitch_name[1:]

   ## find octave
   octave = int(math.floor(number / 12)) + 4

   ## return uninque letter, accidental, octave triple
   return letter, accidental, octave
