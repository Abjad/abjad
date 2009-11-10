from abjad.component import _Component
from abjad.spanners import Spanner


def iterate_components_backwards(spanner, klass = _Component):
   '''.. versionadded:: 1.1.2

   Yield components in `spanner` one at a time from left to right. ::

      abjad> t = Staff(construct.scale(4))
      abjad> p = Beam(t[2:])
      abjad> notes = spannertools.iterate_components_backwards(p, class = Note)
      abjad> for note in notes:
         print note
      Note(f', 8)
      Note(e', 8)

   .. todo:: rename ``spannertools.iterate_components_backward()``.
   '''

   if not isinstance(spanner, Spanner):
      raise TypeError

   for component in reversed(spanner._components):
      for node in component._navigator._DFS(direction = 'right'):
         if isinstance(node, klass):
            yield node
