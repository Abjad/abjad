from abjad.component import _Component
from abjad.spanners import Spanner


def iterate_components_backward(spanner, klass = _Component):
   '''.. versionadded:: 1.1.2

   Yield components in `spanner` one at a time from left to right. ::

      abjad> t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
      abjad> p = Beam(t[2:])
      abjad> notes = spannertools.iterate_components_backward(p, class = Note)
      abjad> for note in notes:
         print note
      Note(f', 8)
      Note(e', 8)
   '''

   if not isinstance(spanner, Spanner):
      raise TypeError

   for component in reversed(spanner._components):
      for node in component._navigator._DFS(direction = 'right'):
         if isinstance(node, klass):
            yield node
