from abjad.helpers.get_spanners_and_indices import _get_spanners_and_indices
from abjad import *


def test_get_spanners_and_indices_01( ):
   '''Return unordered set of spanner, index pairs.
      Give the index of component within each spanner 
      attaching to component.'''

   t = RigidMeasure((5, 8), scale(5))
   beam = Beam(t[:])
   crescendo = Crescendo(t[:])
   glissando = Glissando(t[:])

   result = _get_spanners_and_indices(t[2])

   assert len(result) == 3
   assert (beam, 2) in result
   assert (crescendo, 2) in result
   assert (glissando, 2) in result


def test_get_spanners_and_indices_02( ):
   '''Return empty set when no spanners attach to component.'''

   t = Note(0, (1, 4))

   result = _get_spanners_and_indices(t)

   assert result == set([ ])
