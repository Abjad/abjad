from abjad import *


def test_spannertools_iterate_components_forward_in_spanner_01( ):

   t = Staff(macros.scale(4))
   spanner = BeamSpanner(t[2:])

   notes = spannertools.iterate_components_forward_in_spanner(spanner, klass = Note)
   assert list(notes) == t[2:]
