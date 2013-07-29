from abjad import *


def test_leaftools_fuse_leaves_in_tie_chain_by_immediate_parent_01():
    '''Fuse leaves in tie chain with same immediate parent.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    spannertools.TieSpanner(t.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
      {
            \time 2/8
            c'8 ~
            c'8 ~
      }
      {
            \time 2/8
            c'8 ~
            c'8
      }
    }
    '''

    result = leaftools.fuse_leaves_in_tie_chain_by_immediate_parent(
        t.select_leaves()[1].select_tie_chain())

    r'''
    \new Staff {
      {
            \time 2/8
            c'4 ~
      }
      {
            \time 2/8
            c'4
      }
    }
    '''

    assert inspect(t).is_well_formed()
    assert len(result) == 2
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'4 ~\n\t}\n\t{\n\t\t\\time 2/8\n\t\tc'4\n\t}\n}"


def test_leaftools_fuse_leaves_in_tie_chain_by_immediate_parent_02():
    '''Fuse leaves in tie chain with same immediate parent.
    '''

    t = Staff(notetools.make_repeated_notes(4))
    spannertools.TieSpanner(t.select_leaves())

    r'''
    \new Staff {
            c'8 ~
            c'8 ~
            c'8 ~
            c'8
    }
    '''

    result = leaftools.fuse_leaves_in_tie_chain_by_immediate_parent(
        t.select_leaves()[1].select_tie_chain())

    assert inspect(t).is_well_formed()
    assert len(result) == 1
    assert t.lilypond_format == "\\new Staff {\n\tc'2\n}"


def test_leaftools_fuse_leaves_in_tie_chain_by_immediate_parent_03():
    '''Fuse leaves in tie chain with same immediate parent.
    '''

    t = Note("c'4")
    result = leaftools.fuse_leaves_in_tie_chain_by_immediate_parent(
        t.select_tie_chain())
    assert len(result) == 1
    assert inspect(t).is_well_formed()
