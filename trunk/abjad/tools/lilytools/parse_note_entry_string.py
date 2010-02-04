from _parse_note_entry_token import _parse_note_entry_token
from abjad.container import Container
import re


def parse_note_entry_string(note_entry_string):
   '''.. versionadded:: 1.1.2

   Parse simple LilyPond `note_entry_string`.
   '''

   container = Container([ ])
   tokens = note_entry_string.split( ) 
   tie_started = False
   for token in tokens:
      if re.match('\w+', token) is not None: 
         abjad_object = _parse_note_entry_token(token)
         last_leaf = iterate.leaves_backward_in(container, -1)
         last_leaf.splice(abjad_object)
      elif token == '~':
         last_leaf = iterate.leaves_backward_in(container, -1)
         Tie([last_leaf])
         tie_started = True
      else:
         pass

   result = container[:]
   container[:] = [ ]

   return result
