from abjad.exceptions import PitchError
import re


def tick_string_to_octave_number(tick_string):
   '''.. versionadded:: 1.1.2

   Convert European `tick_string` to American octave number. ::

      abjad> pitchtools.tick_string_to_octave_number('')
      3

   ::

      abjad> pitchtools.tick_string_to_octave_number("'")
      4
   '''

   if not isinstance(tick_string, str):
      raise TypeError('tick string must be string.')

   if tick_string == '':
      return 3
   elif re.match("(\\'+)", tick_string):
      return 3 + len(tick_string)
   elif re.match('(\\,+)', tick_string):
      return 3 - len(tick_string)
   else:
      PitchError('incorrect tick string format.')
