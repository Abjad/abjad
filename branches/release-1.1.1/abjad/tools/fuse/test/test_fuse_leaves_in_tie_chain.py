from abjad import *


def test_fuse_leaves_in_tie_chain_01( ):
   '''Fuse leaves in tie chain with same immediate parent.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
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

   result = fuse.leaves_in_tie_chain(t.leaves[1].tie.chain)

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

   assert check.wf(t)
   assert len(result) == 2
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'4 ~\n\t}\n\t{\n\t\t\\time 2/8\n\t\tc'4\n\t}\n}"


def test_fuse_leaves_in_tie_chain_02( ):
   '''Fuse leaves in tie chain with same immediate parent.'''

   t = Staff(construct.run(4))
   Tie(t.leaves)
   
   r'''
   \new Staff {
         c'8 ~
         c'8 ~
         c'8 ~
         c'8
   }
   '''

   result = fuse.leaves_in_tie_chain(t.leaves[1].tie.chain)

   assert check.wf(t)
   assert len(result) == 1
   assert t.format == "\\new Staff {\n\tc'2\n}"


def test_fuse_leaves_in_tie_chain_03( ):
   '''Fuse leaves in tie chain with same immediate parent.'''

   t = Note(0, (1, 4))
   result = fuse.leaves_in_tie_chain(t.tie.chain)
   assert len(result) == 1
   assert check.wf(t)
