from abjad import *


def test_SequentialLeafSelection__attach_tie_spanner_to_leaf_pair_01():
    '''Span left leaf with spanner and right leaf without spanner.
    '''

    t = Voice(notetools.make_repeated_notes(4))
    spannertools.TieSpanner(t[:2])

    r'''
    \new Voice {
        c'8 ~
        c'8
        c'8
        c'8
    }
    '''

    t.select_leaves()[1:3]._attach_tie_spanner_to_leaf_pair()

    r'''
    \new Voice {
        c'8 ~
        c'8 ~
        c'8
        c'8
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\new Voice {\n\tc'8 ~\n\tc'8 ~\n\tc'8\n\tc'8\n}"


def test_SequentialLeafSelection__attach_tie_spanner_to_leaf_pair_02():
    '''Span left leaf with spanner and right leaf with spanner.
    '''

    t = Voice(notetools.make_repeated_notes(4))
    spannertools.TieSpanner(t[:2])
    spannertools.TieSpanner(t[2:])

    r'''
    \new Voice {
        c'8 ~
        c'8
        c'8 ~
        c'8
    }
    '''

    t.select_leaves()[1:3]._attach_tie_spanner_to_leaf_pair()

    r'''
    \new Voice {
        c'8 ~
        c'8 ~
        c'8 ~
        c'8
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\new Voice {\n\tc'8 ~\n\tc'8 ~\n\tc'8 ~\n\tc'8\n}"


def test_SequentialLeafSelection__attach_tie_spanner_to_leaf_pair_03():
    '''Span left leaves with no spanner.
    '''

    t = Voice(notetools.make_repeated_notes(4))

    r'''
    \new Voice {
        c'8
        c'8
        c'8
        c'8
    }
    '''

    t.select_leaves()[1:3]._attach_tie_spanner_to_leaf_pair()

    r'''
    \new Voice {
        c'8
        c'8 ~
        c'8
        c'8
    }
    '''

    assert select(t).is_well_formed()
    assert t.lilypond_format == "\\new Voice {\n\tc'8\n\tc'8 ~\n\tc'8\n\tc'8\n}"
