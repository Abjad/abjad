from abjad.exceptions import PitchError
import re


def octave_tick_string_to_octave_number(tick_string):
   '''.. versionadded:: 1.1.2

   Convert European `tick_string` to American octave number. ::

      abjad> pitchtools.octave_tick_string_to_octave_number('')
      3

   ::

      abjad> pitchtools.octave_tick_string_to_octave_number("'")
      4

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.tick_string_to_octave_number( )`` to
      ``pitchtools.octave_tick_string_to_octave_number( )``.
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
