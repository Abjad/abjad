from abjad import *


def test_tietools_group_leaves_in_tie_chain_by_immediate_parents_01():
    '''Group leaves in tie chain by immediate parent.'''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    tietools.TieSpanner(t.leaves)

    r'''
    \new Staff {
            \time 2/8
            c'8 ~
            c'8 ~
            \time 2/8
            c'8 ~
            c'8
    }
    '''

    parts = tietools.group_leaves_in_tie_chain_by_immediate_parents(
        tietools.get_tie_chain(t.leaves[0]))

    assert len(parts) == 2
    assert parts[0] == list(t.leaves[:2])
    assert parts[1] == list(t.leaves[2:])


def test_tietools_group_leaves_in_tie_chain_by_immediate_parents_02():
    '''Group leaves in tie chain by immediate parent.'''

    t = Staff(notetools.make_repeated_notes(4))
    tietools.TieSpanner(t.leaves)

    r'''
    \new Staff {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
    }
    '''

    parts = tietools.group_leaves_in_tie_chain_by_immediate_parents(
        tietools.get_tie_chain(t.leaves[0]))

    assert len(parts) == 1
    assert parts[0] == list(t.leaves)


def test_tietools_group_leaves_in_tie_chain_by_immediate_parents_03():
    '''Group leaves in tie chain by immediate parent.'''

    t = Note("c'4")

    parts = tietools.group_leaves_in_tie_chain_by_immediate_parents(tietools.get_tie_chain(t))

    assert len(parts) == 1
    assert parts[0] == [t]
