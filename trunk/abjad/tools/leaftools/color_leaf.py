from abjad.components.Chord import Chord
from abjad.components.Note import Note
from abjad.components.Rest import Rest


def color_leaf(leaf, color):
   r'''.. versionadded:: 1.1.2

   Color `leaf` with `color`::

      abjad> staff = Staff(macros.scale(4))
      abjad> BeamSpanner(staff.leaves)
      abjad> f(staff)
      \new Staff {
         c'8 [
         d'8
         e'8
         f'8 ]
      }
      
   ::
      
      abjad> leaftools.color_leaf(staff[0], 'red')
      Note(c', 8)

   ::

      abjad> f(staff)
      \new Staff {
         \once \override Accidental #'color = #red
         \once \override Dots #'color = #red
         \once \override NoteHead #'color = #red
         c'8 [
         d'8
         e'8
         f'8 ]
      }

   Return `leaf`.
   '''

   ## color leaf
   if isinstance(leaf, (Note, Chord)):
      leaf.override.accidental.color = color
      leaf.override.dots.color = color
      leaf.override.note_head.color = color
   elif isinstance(leaf, Rest):
      leaf.override.dots.color = color
      leaf.override.rest.color = color

   ## return leaf
   return leaf
