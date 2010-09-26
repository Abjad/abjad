from abjad.exceptions import PitchError
import re


def pitch_name_to_pitch_class_name(pitch_string):
   '''.. versionadded:: 1.1.2

   Convert `pitch_string` to pitch name. ::

      abjad> pitchtools.pitch_name_to_pitch_class_name('cs,,,')
      'cs'

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.pitch_string_to_name( )`` to
      ``pitchtools.pitch_name_to_pitch_class_name( )``.
   '''

   if not isinstance(pitch_string, str):
      raise TypeError('pitch string must be string.')

   match = re.match('^([a-z]+)(\,*|\'*)$', pitch_string)
   if match is None:
      raise PitchError('incorrect pitch string format: "%s".' % pitch_string)

   name, octave_number = match.groups( )

   return name
