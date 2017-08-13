import abjad


def test_spannertools_PhrasingSlur___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = abjad.PhrasingSlur()
    spanner_2 = abjad.PhrasingSlur()

    assert not spanner_1 == spanner_2
