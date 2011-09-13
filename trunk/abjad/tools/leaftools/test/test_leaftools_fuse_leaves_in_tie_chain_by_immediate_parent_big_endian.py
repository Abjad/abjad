from abjad import *


def test_leaftools_fuse_leaves_in_tie_chain_by_immediate_parent_big_endian_01():
    '''Fuse leaves in tie chain with same immediate parent.'''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    tietools.TieSpanner(t.leaves)

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

    result = leaftools.fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(
      tietools.get_tie_chain(t.leaves[1]))

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

    assert componenttools.is_well_formed_component(t)
    assert len(result) == 2
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'4 ~\n\t}\n\t{\n\t\t\\time 2/8\n\t\tc'4\n\t}\n}"


def test_leaftools_fuse_leaves_in_tie_chain_by_immediate_parent_big_endian_02():
    '''Fuse leaves in tie chain with same immediate parent.'''

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

    result = leaftools.fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(
      tietools.get_tie_chain(t.leaves[1]))

    assert componenttools.is_well_formed_component(t)
    assert len(result) == 1
    assert t.format == "\\new Staff {\n\tc'2\n}"


def test_leaftools_fuse_leaves_in_tie_chain_by_immediate_parent_big_endian_03():
    '''Fuse leaves in tie chain with same immediate parent.'''

    t = Note("c'4")
    result = leaftools.fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(
      tietools.get_tie_chain(t))
    assert len(result) == 1
    assert componenttools.is_well_formed_component(t)
