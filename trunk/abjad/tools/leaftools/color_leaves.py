from abjad.chord import Chord
from abjad.note import Note
from abjad.rest import Rest
from abjad.tools import iterate


def color_leaves(expr, color):
   r'''.. versionadded:: 1.1.2

   Iterate leaves forward in `expr` and color note heads, rests, dots
   and accidentals according to `color`. ::

      abjad> t = Staff([Note(1, (3, 16)), Rest((3, 16)), Skip((3, 16)), Chord([0, 1, 9], (3, 16))])
      abjad> leaftools.color_leaves(t, 'red')
      abjad> f(t)
      \new Staff {
              \once \override Accidental #'color = #red
              \once \override Dots #'color = #red
              \once \override NoteHead #'color = #red
              cs'8.
              \once \override Dots #'color = #red
              \once \override Rest #'color = #red
              r8.
              s8.
              \once \override Accidental #'color = #red
              \once \override Dots #'color = #red
              \once \override NoteHead #'color = #red
              <c' cs' a'>8.
      }
   '''

   for leaf in iterate.leaves_forward_in(expr):
      if isinstance(leaf, (Note, Chord)):
         leaf.accidental.color = color
         leaf.dots.color = color
         leaf.note_head.color = color
      elif isinstance(leaf, Rest):
         leaf.dots.color = color
         leaf.rest.color = color
