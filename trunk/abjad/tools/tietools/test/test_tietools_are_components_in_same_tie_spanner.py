from abjad import *


def test_tietools_are_components_in_same_tie_spanner_01():
    '''True if all components in list share same tie spanner.'''

    t = Voice(notetools.make_repeated_notes(4))
    tietools.TieSpanner(t[:2])

    r'''
    \new Voice {
        c'8 ~
        c'8
        c'8
        c'8
    }
    '''

    assert tietools.are_components_in_same_tie_spanner(t[:2])
    assert not tietools.are_components_in_same_tie_spanner(t[-2:])
    assert tietools.are_components_in_same_tie_spanner(t[:1])
    assert not tietools.are_components_in_same_tie_spanner(t[-1:])
    assert not tietools.are_components_in_same_tie_spanner(t[:])
