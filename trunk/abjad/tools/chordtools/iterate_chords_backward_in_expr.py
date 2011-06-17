from abjad.tools.chordtools.Chord import Chord


def iterate_chords_backward_in_expr(expr, start = 0, stop = None):
   r'''.. versionadded:: 1.1.2

   Iterate chords backward in `expr`::

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
      Chord("<e' g' c''>8")

   Ignore threads.

   Return generator.
   '''
   from abjad.tools import componenttools
   
   return componenttools.iterate_components_backward_in_expr(
      expr, Chord, start = start, stop = stop)
