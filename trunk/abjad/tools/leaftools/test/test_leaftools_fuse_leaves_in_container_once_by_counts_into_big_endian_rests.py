from abjad import *


def test_fuse_contents_by_counts_04( ):
   '''Glom voice into rests.'''

   t = Voice(leaftools.make_repeated_notes(5))
   #fuse.contents_by_counts(t, [1, 2, 2], Rest)
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
