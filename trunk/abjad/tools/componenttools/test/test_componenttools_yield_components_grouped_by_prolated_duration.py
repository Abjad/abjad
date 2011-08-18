from abjad import *
import py.test


def test_componenttools_yield_components_grouped_by_prolated_duration_01():

    notes = notetools.make_notes(
        [0], [(1, 4), (1, 4), (1, 8), (1, 16), (1, 16), (1, 16)])
    groups = componenttools.yield_components_grouped_by_prolated_duration(notes)

    assert groups.next() == (notes[0], notes[1])
    assert groups.next() == (notes[2], )
    assert groups.next() == (notes[3], notes[4], notes[5])
    assert py.test.raises(StopIteration, 'groups.next()')
