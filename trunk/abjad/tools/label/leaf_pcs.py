from abjad.tools import iterate
from abjad.tools import pitchtools


def leaf_pcs(expr, number = True, color = False):
   r'''Iterate *expr* and label all leaf pitch classes.

   When ``number = True`` add markup below leaves.

   ::

      abjad> t = Staff(construct.scale(4))
      abjad> label.leaf_pcs(t)
      abjad> print t.format
      \new Staff {
         c'8 _ \markup { \small 0 }
         d'8 _ \markup { \small 2 }
         e'8 _ \markup { \small 4 }
         f'8 _ \markup { \small 5 }
      }

   When ``color = True`` call :func:`~abjad.tools.pitchtools.color_by_pc`.

   ::

      abjad> t = Staff(construct.scale(4))
      abjad> label.leaf_pcs(t)
      abjad> print t.format
      \new Staff {
         \once \override NoteHead #'color = #(x11-color 'red)
         c'8
         \once \override NoteHead #'color = #(x11-color 'orange)
         d'8
         \once \override NoteHead #'color = #(x11-color 'ForestGreen)
         e'8
         \once \override NoteHead #'color = #(x11-color 'MediumOrchid)
         f'8
      }

   You can of course set *number* and *color* at the same time.
   '''

   from abjad.note import Note
   for note in iterate.naive(expr, Note):
      if number:
         label = r'\small %s' % note.pitch.pc
         note.markup.down.append(label)
      if color:
         pitchtools.color_by_pc(note)
