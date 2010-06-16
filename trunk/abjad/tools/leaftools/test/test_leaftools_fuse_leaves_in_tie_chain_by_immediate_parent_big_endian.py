from abjad import *


def test_leaftools_fuse_leaves_in_tie_chain_by_immediate_parent_big_endian_01( ):
   '''Fuse leaves in tie chain with same immediate parent.'''

   t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2)
   Tie(t.leaves)
   
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

   result = leaftools.fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(t.leaves[1].tie.chain)

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


def test_leaftools_fuse_leaves_in_tie_chain_by_immediate_parent_big_endian_02( ):
   '''Fuse leaves in tie chain with same immediate parent.'''

   t = Staff(leaftools.make_repeated_notes(4))
   Tie(t.leaves)
   
   r'''
   \new Staff {
         c'8 ~
         c'8 ~
         c'8 ~
         c'8
   }
   '''

   result = leaftools.fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(t.leaves[1].tie.chain)

   assert componenttools.is_well_formed_component(t)
   assert len(result) == 1
   assert t.format == "\\new Staff {\n\tc'2\n}"


def test_leaftools_fuse_leaves_in_tie_chain_by_immediate_parent_big_endian_03( ):
   '''Fuse leaves in tie chain with same immediate parent.'''

   t = Note(0, (1, 4))
   result = leaftools.fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(t.tie.chain)
   assert len(result) == 1
   assert componenttools.is_well_formed_component(t)
