from abjad import *


def test_tietools_are_components_in_same_tie_spanner_01():
    '''True if all components share same tie spanner.
    '''

    t = Voice("c'8 ~ c' c' c'")

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
