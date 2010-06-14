from abjad.chord import Chord
from abjad.note import Note
from abjad.rest import Rest


def color_leaf(leaf, color):
   r'''.. versionadded:: 1.1.2

   Color `leaf` with `color`::

      abjad> staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> Beam(staff.leaves)
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
      leaf.accidental.color = color
      leaf.dots.color = color
      leaf.note_head.color = color
   elif isinstance(leaf, Rest):
      leaf.dots.color = color
      leaf.rest.color = color

   ## return leaf
   return leaf
