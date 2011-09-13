from abjad import *


def test_tietools_is_component_with_tie_spanner_attached_01():

    staff = Staff(notetools.make_repeated_notes(4))
    tietools.TieSpanner(staff[:])

    r'''
    \new Staff {
        c'8 ~
        c'8 ~
        c'8 ~
        c'8
    }
    '''

    assert tietools.is_component_with_tie_spanner_attached(staff[1])

    assert not tietools.is_component_with_tie_spanner_attached(staff)
