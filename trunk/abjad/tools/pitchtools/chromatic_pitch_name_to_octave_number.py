from abjad.exceptions import PitchError
from abjad.tools.pitchtools.octave_tick_string_to_octave_number import \
   octave_tick_string_to_octave_number
import re


def chromatic_pitch_name_to_octave_number(pitch_string):
   '''.. versionadded:: 1.1.2

   Convert `pitch_string` to American octave number. ::

      abjad> pitchtools.chromatic_pitch_name_to_octave_number('cs')
      3

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_string_to_octave_number( )`` to
      ``pitchtools.chromatic_pitch_name_to_octave_number( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_name_to_octave_number( )`` to
      ``pitchtools.chromatic_pitch_name_to_octave_number( )``.
   '''

   if not isinstance(pitch_string, str):
      raise TypeError('pitch string must be string.')

   match = re.match('^([a-z]+)(\,*|\'*)$', pitch_string)
   if match is None:
      raise PitchError('incorrect pitch string format.')

   name, tick_string = match.groups( )
   octave_number = octave_tick_string_to_octave_number(tick_string)

   return octave_number
