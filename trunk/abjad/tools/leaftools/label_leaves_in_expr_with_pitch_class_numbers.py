from abjad.tools import componenttools
from abjad.tools import markuptools
from abjad.tools import notetools
from abjad.tools import threadtools


def label_leaves_in_expr_with_pitch_class_numbers(expr, number = True, color = False, 
   markup_direction = 'down'):
   r'''Label the pitch-class of every leaf in `expr`.

   When ``number = True`` add markup below leaves.

   ::

      abjad> t = Staff(macros.scale(4))
      abjad> leaftools.label_leaves_in_expr_with_pitch_class_numbers(t)
      abjad> print t.format
      \new Staff {
         c'8 _ \markup { \small 0 }
         d'8 _ \markup { \small 2 }
         e'8 _ \markup { \small 4 }
         f'8 _ \markup { \small 5 }
      }

   When ``color = True`` call :func:`~abjad.tools.notetools.color_note_head_by_numeric_chromatic_pitch_class_color_map`.

   ::

      abjad> t = Staff(macros.scale(4))
      abjad> leaftools.label_leaves_in_expr_with_pitch_class_numbers(t)
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

   You can of course set `number` and `color` at the same time.

   .. versionchanged:: 1.1.2
      renamed ``label.leaf_pcs( )`` to
      ``leaftools.label_leaves_in_expr_with_pitch_class_numbers( )``.
   '''

   from abjad.components import Note
   for note in componenttools.iterate_components_forward_in_expr(expr, Note):
      if number:
         label = r'\small %s' % abs(note.pitch.numbered_chromatic_pitch_class)
         markuptools.Markup(label, markup_direction)(note)
      if color:
         notetools.color_note_head_by_numeric_chromatic_pitch_class_color_map(note)
