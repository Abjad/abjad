from abjad.components import Chord
from abjad.components import Note
from abjad.tools import componenttools


def iterate_notes_and_chords_backward_in_expr(expr, start = 0, stop = None):
   r'''.. versionadded:: 1.1.2

   Iterate notes and chords backward in `expr`::

      abjad> staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")

   ::

      abjad> f(staff)
      \new Staff {
         <e' g' c''>8
         a'8
         r8
         <d' f' b'>8
         r2
      }

   ::

      abjad> for chord in chordtools.iterate_chords_backward_in_expr(staff):
      ...   chord
      Chord("<d' f' b'>8")
      Note("a'8")
      Chord("<e' g' c''>8")

   Ignore threads.

   Return generator.
   '''
   
   return componenttools.iterate_components_backward_in_expr(
      expr, (Note, Chord), start = start, stop = stop)
