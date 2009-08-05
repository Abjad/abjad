from abjad import *


def test_tietools_group_by_parent_01( ):
   '''Group leaves in tie chain by immediate parent.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   Tie(t.leaves)

   r'''
   \new Staff {
         \time 2/8
         c'8 ~
         c'8 ~
         \time 2/8
         c'8 ~
         c'8
   }
   '''

   parts = tietools.group_by_parent(t.leaves[0].tie.chain)
   
   assert len(parts) == 2
   assert parts[0] == list(t.leaves[:2])
   assert parts[1] == list(t.leaves[2:])


def test_tietools_group_by_parent_02( ):
   '''Group leaves in tie chain by immediate parent.'''

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

   parts = tietools.group_by_parent(t.leaves[0].tie.chain)
   
   assert len(parts) == 1
   assert parts[0] == list(t.leaves)


def test_tietools_group_by_parent_03( ):
   '''Group leaves in tie chain by immediate parent.'''

   t = Note(0, (1, 4))
   
   parts = tietools.group_by_parent(t.tie.chain)
   
   assert len(parts) == 1
   assert parts[0] == [t]
