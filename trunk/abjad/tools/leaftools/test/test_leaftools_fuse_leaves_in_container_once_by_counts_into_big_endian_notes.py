from abjad import *


def test_leaftools_fuse_leaves_in_container_once_by_counts_into_big_endian_notes_01():
    '''Glom voice.'''

    t = Voice(notetools.make_repeated_notes(5, Duration(1, 16)))
    spannertools.SlurSpanner(t[:])
    leaftools.fuse_leaves_in_container_once_by_counts_into_big_endian_notes(t, [1, 2, 2])

    r'''
    \new Voice {
      c'16 (
      c'8
      c'8 )
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'16 (\n\tc'8\n\tc'8 )\n}"


def test_leaftools_fuse_leaves_in_container_once_by_counts_into_big_endian_notes_02():
    '''Glom voice and render big-endian tied values.'''

    t = Voice(notetools.make_repeated_notes(5))
    spannertools.SlurSpanner(t[:])
    leaftools.fuse_leaves_in_container_once_by_counts_into_big_endian_notes(t, [5])

    r'''
    \new Voice {
      c'2 ( ~
      c'8 )
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'2 ( ~\n\tc'8 )\n}"
