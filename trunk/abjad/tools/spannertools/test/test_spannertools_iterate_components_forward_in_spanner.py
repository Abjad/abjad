from abjad import *


def test_spannertools_iterate_components_forward_in_spanner_01():

    t = Staff("c'8 d'8 e'8 f'8")
    spanner = spannertools.BeamSpanner(t[2:])

    notes = spannertools.iterate_components_forward_in_spanner(spanner, klass = Note)
    assert list(notes) == t[2:]
