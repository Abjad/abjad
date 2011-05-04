from abjad.components import Chord
from abjad.components import Note
from abjad.tools import componenttools


def iterate_notes_and_chords_forward_in_expr(expr, start = 0, stop = None):
   r'''.. versionadded:: 1.1.2

   Iterate notes and chords forward in `expr`::

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

      abjad> for chord in chordtools.iterate_chords_forward_in_expr(staff):
      ...   chord
      Chord("<e' g' c''>8")
      Note("a'8")
      Chord("<d' f' b'>8")

   Ignore threads.

   Return generator.
   '''
   
   return componenttools.iterate_components_forward_in_expr(
      expr, (Note, Chord), start = start, stop = stop)
