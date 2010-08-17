from abjad.components.Container import Container
from abjad.exceptions import MissingSpannerError
from abjad.marks.Articulation import Articulation
from abjad.tools.spannertools import SlurSpanner
from abjad.tools.spannertools import TieSpanner
from abjad.tools.lilyfiletools._parse_note_entry_token import _parse_note_entry_token
from abjad.tools.lilyfiletools._parse_chord_entry_token import _parse_chord_entry_token
from abjad.components.Voice import Voice
import re


def parse_note_entry_string(note_entry_string):
   '''.. versionadded:: 1.1.2

   Parse LilyPond `note_entry_string`::

      abjad> note_entry_string = "g'2 a'2 g'4. fs'8 e'4 d'4"
      abjad> lilyfiletools.parse_note_entry_string(note_entry_string)
      {g'4, a'4, a'2, fs'8, e'4, d'4}

   Return Abjad container of note, rest and chord instances.

   Do not parse tuplets, measures or other complex LilyPond input.
   '''
   from abjad.tools import leaftools

   container = Container([ ])
   tokens = note_entry_string.split( ) 

   is_chord = False
   chord_tokens = [ ]

   in_slur = False
   slur_start_leaf = None

   tie_next_leaf = False
   waiting_on_bar_string = False

   for token in tokens:

      if is_chord: # we are inside a chord

         if re.match("[A-Za-z0-9,']+>[0-9]+", token) is not None:
            chord_tokens.append(token)
            leaf = _parse_chord_entry_token(' '.join(chord_tokens))
            if tie_next_leaf:
               last_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
               last_leaf.splice([leaf])
               tie_next_leaf = False
            else:
               container.append(leaf)
            is_chord = False
            chord_tokens = [ ]

         elif re.match('\w+', token) is not None:
            chord_tokens.append(token)

         else:
            pass

      else:

         if re.match('\w+', token) is not None:
            leaf = _parse_note_entry_token(token)
            if tie_next_leaf:
               last_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
               last_leaf.splice([leaf])
               tie_next_leaf = False
            else:
               container.append(leaf) 

         elif re.match('<\w+', token) is not None:
            is_chord = True
            chord_tokens.append(token)

         elif token == '~':
            last_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
            try:
               tie_spanner = last_leaf.tie.spanner
            except MissingSpannerError:
               TieSpanner([last_leaf])
            tie_next_leaf = True

         elif token == r'\bar':
            waiting_on_bar_string = True

         elif token.startswith('"'):
            bar_string = eval(token)
            last_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
            last_leaf.misc.bar = bar_string
            waiting_on_bar_string = False

         elif token.startswith(('\\', '-', '^', '_')):
            last_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
            try:
               if 0 <= token.index('\\'):
                  last_leaf.articulations.append(token)
            except:
               last_leaf.articulations.append(Articulation(token[1], token[0]))

         elif token == '(':
            if in_slur:
               raise Exception('Opening a slur when another is already open.')
            in_slur = True
            slur_start_leaf = leaftools.get_nth_leaf_in_expr(container, -1)

         elif token == ')':
            if not in_slur:
               raise Exception('Closing a non-existent slur.')
            in_slur = False
            slur_stop_leaf = leaftools.get_nth_leaf_in_expr(container, -1)
            start_index = container.index(slur_start_leaf)
            stop_index = container.index(slur_stop_leaf)
            SlurSpanner(container[start_index:stop_index + 1])
            slur_start_leaf = None

         else:
            pass


   return container
