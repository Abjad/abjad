from abjad.exceptions import PitchError
from tick_string_to_octave_number import tick_string_to_octave_number
import re


def pitch_string_to_octave_number(pitch_string):
   '''.. versionadded:: 1.1.2

   Convert `pitch_string` to American octave number. ::

      abjad> pitchtools.pitch_string_to_name('cs')
      3
   '''

   if not isinstance(pitch_string, str):
      raise TypeError('pitch string must be string.')

   match = re.match('^([a-z]+)(\,*|\'*)$', pitch_string)
   if match is None:
      raise PitchError('incorrect pitch string format.')

   name, tick_string = match.groups( )
   octave_number = tick_string_to_octave_number(tick_string)

   return octave_number
