from abjad import *


def test_leaftoolsfuse_leaves_in_container_once_by_counts_into_little_endian_notes_01():
    '''Glom voice and render big-endian tied values.'''

    t = Voice(notetools.make_repeated_notes(5))
    spannertools.SlurSpanner(t)
    leaftools.fuse_leaves_in_container_once_by_counts_into_little_endian_notes(t, [5])

    r'''
    \new Voice {
      c'8 ( ~
      c'2 )
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\tc'8 ( ~\n\tc'2 )\n}"
