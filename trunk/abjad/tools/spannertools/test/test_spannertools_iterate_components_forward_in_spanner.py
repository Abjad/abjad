from abjad import *


def test_spannertools_iterate_components_forward_in_spanner_01( ):

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   spanner = Beam(t[2:])

   notes = spannertools.iterate_components_forward_in_spanner(spanner, klass = Note)
   assert list(notes) == t[2:]
