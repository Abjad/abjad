from _parse_note_entry_token import _parse_note_entry_token
from abjad.container import Container
from abjad.tools import iterate
import re


def parse_note_entry_string(note_entry_string):
   '''.. versionadded:: 1.1.2

   Parse simple LilyPond `note_entry_string`. ::

      abjad> note_entry_string = "g'2 a'2 g'4. fs'8 e'4 d'4"
      abjad> lilytools.parse_note_entry_string(note_entry_string)
      [Note(g', 2), Note(a', 2), Note(g', 4.), Note(fs', 8), Note(e', 4), Note(d', 4)]
   '''

   container = Container([ ])
   tokens = note_entry_string.split( ) 
   tie_started = False
   for token in tokens:
      if re.match('\w+', token) is not None: 
         abjad_object = _parse_note_entry_token(token)
         last_leaf = iterate.get_nth_leaf(container, -1)
         if last_leaf is not None:
            last_leaf.splice([abjad_object])
         else:
            container.append(abjad_object)
      elif token == '~':
         last_leaf = iterate.leaves_backward_in(container, -1)
         Tie([last_leaf])
         tie_started = True
      else:
         pass

   result = container[:]
   container[:] = [ ]

   return result
