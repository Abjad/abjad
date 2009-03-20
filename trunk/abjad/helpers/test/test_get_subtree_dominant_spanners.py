from abjad import *
from abjad.helpers.get_subtree_dominant_spanners import _get_subtree_dominant_spanners


def test_get_subtree_dominant_spanners_01( ):
   '''Return list of all spanners attached to component or
      attached to any of the children of component with
      begin time less than or equal to begin time of component and
      end time greater than or equal to end time of component.'''

   t = Voice(scale(4))
   beam = Beam(t[:2])
   glissando = Glissando(t[2:])
   trill = Trill(t[:])

   spanners = _get_subtree_dominant_spanners(t)

   assert beam not in spanners
   assert glissando not in spanners
   assert trill in spanners
