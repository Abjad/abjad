from abjad import *


def test_spannertools_iterate_components_forward_01( ):

   t = Staff(construct.scale(4))
   spanner = Beam(t[2:])

   notes = spannertools.iterate_components_forward(spanner, klass = Note)
   assert list(notes) == t[2:]
