from abjad.exceptions import InputSpecificationError
from abjad.note import Note
from abjad.pitch import Pitch
from abjad.rest import Rest
from abjad.skip import Skip
from abjad.tools import durtools
from abjad.tools import pitchtools
import re


def _parse_note_entry_token(note_entry_token):
   '''.. versionadded:: 1.1.2

   Parse simple LilyPond `note_entry_token`. ::

      abjad> _parse_note_entry_token("c'4.")
      Note(c', 4.)

   ::

      abjad> _parse_note_entry_token('r8')  
      Rest(8)
   '''

   if not isinstance(note_entry_token, str):
      raise TypeError('LilyPond input token must be string.')

   numeric_body_strings = [str(2 ** n) for n in range(8)]
   other_body_strings = [r'\\breve', r'\\longa', r'\\maxima']
   body_strings = numeric_body_strings + other_body_strings
   body_strings = '|'.join(body_strings)
   pattern = '^([a-z]+)(\,*|\'*)\s*(%s)(\\.*)$' % body_strings

   match = re.match(pattern, note_entry_token)
   if match is None:
      message = 'incorrect note entry token %s.' % note_entry_token
      raise InputSpecificationError(message)

   name, ticks, duration_body, dots = match.groups( )

   duration_string = duration_body + dots
   duration = durtools.duration_string_to_rational(duration_string)

   if name == 'r':
      return Rest(duration)
   elif name == 's':
      return Skip(duration)
   else:
      pitch_string = name + ticks
      pitch = Pitch(pitch_string)
      return Note(pitch, duration)
