from abjad.container import Container
from abjad.exceptions import MissingSpannerError
from abjad.spanners import Tie
from abjad.tools import iterate
from abjad.tools.lilytools._parse_note_entry_token import \
   _parse_note_entry_token
from abjad.voice import Voice
import re


def parse_note_entry_string(note_entry_string):
   '''.. versionadded:: 1.1.2

   Parse LilyPond `note_entry_string`::

      abjad> note_entry_string = "g'2 a'2 g'4. fs'8 e'4 d'4"
      abjad> lilytools.parse_note_entry_string(note_entry_string)
      {g'4, a'4, a'2, fs'8, e'4, d'4}

   Return Abjad container of note, rest and chord instances.

   Do not parse tuplets, measures or other complex LilyPond input.
   '''

   container = Container([ ])
   tokens = note_entry_string.split( ) 
   tie_next_leaf = False
   waiting_on_bar_string = False
   for token in tokens:
      if re.match('\w+', token) is not None: 
         leaf = _parse_note_entry_token(token)
         if tie_next_leaf:
            last_leaf = iterate.get_nth_leaf_in_expr(container, -1)
            last_leaf.splice([leaf])
            tie_next_leaf = False
         else:
            container.append(leaf) 
      elif token == '~':
         last_leaf = iterate.get_nth_leaf_in_expr(container, -1)
         try:
            tie_spanner = last_leaf.tie.spanner
         except MissingSpannerError:
            Tie([last_leaf])
         tie_next_leaf = True
      elif token == r'\bar':
         waiting_on_bar_string = True
      elif token.startswith('"'):
         bar_string = eval(token)
         last_leaf = iterate.get_nth_leaf_in_expr(container, -1)
         last_leaf.bar_line.kind = bar_string
         waiting_on_bar_string = False
      elif token.startswith('\\'):
         last_leaf = iterate.get_nth_leaf_in_expr(container, -1)
         articulation_string = token.strip('\\')
         last_leaf.articulations.append(articulation_string)
      else:
         pass

   return container
