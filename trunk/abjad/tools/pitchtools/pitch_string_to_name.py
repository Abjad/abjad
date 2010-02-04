from abjad.exceptions import PitchError
import re


def pitch_string_to_name(pitch_string):
   '''.. versionadded:: 1.1.2

   Convert `pitch_string` to pitch name. ::

      abjad> pitchtools.pitch_string_to_name('cs,,,')
      'cs'
   '''

   if not isinstance(pitch_string, str):
      raise TypeError('pitch string must be string.')

   match = re.match('^([a-z]+)(\,*|\'*)$', pitch_string)
   if match is None:
      raise PitchError('incorrect pitch string format.')

   name, octave_number = match.groups( )

   return name
