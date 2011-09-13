from abjad import *


def test_leaftools_fuse_leaves_in_container_once_by_counts_into_big_endian_rests_01():
    '''Glom voice into rests.'''

    t = Voice(notetools.make_repeated_notes(5))
    leaftools.fuse_leaves_in_container_once_by_counts_into_big_endian_rests(t, [1, 2, 2])

    r'''
    \new Voice {
      r8
      r4
      r4
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == '\\new Voice {\n\tr8\n\tr4\n\tr4\n}'
