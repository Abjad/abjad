from abjad import *


def test_tietools_apply_tie_spanner_to_leaf_pair_01():
    '''Span left leaf with spanner and right leaf without spanner.'''

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

    tietools.apply_tie_spanner_to_leaf_pair(t[1], t[2])

    r'''
    \new Voice {
        c'8 ~
        c'8 ~
        c'8
        c'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 ~\n\tc'8 ~\n\tc'8\n\tc'8\n}"


def test_tietools_apply_tie_spanner_to_leaf_pair_02():
    '''Span left leaf with spanner and right leaf with spanner.'''

    t = Voice(notetools.make_repeated_notes(4))
    tietools.TieSpanner(t[:2])
    tietools.TieSpanner(t[2:])

    r'''
    \new Voice {
        c'8 ~
        c'8
        c'8 ~
        c'8
    }
    '''

    tietools.apply_tie_spanner_to_leaf_pair(t[1], t[2])

    r'''
    \new Voice {
        c'8 ~
        c'8 ~
        c'8 ~
        c'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8 ~\n\tc'8 ~\n\tc'8 ~\n\tc'8\n}"


def test_tietools_apply_tie_spanner_to_leaf_pair_03():
    '''Span left leaves with no spanner.'''

    t = Voice(notetools.make_repeated_notes(4))

    r'''
    \new Voice {
        c'8
        c'8
        c'8
        c'8
    }
    '''

    tietools.apply_tie_spanner_to_leaf_pair(t[1], t[2])

    r'''
    \new Voice {
        c'8
        c'8 ~
        c'8
        c'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'8\n\tc'8 ~\n\tc'8\n\tc'8\n}"
