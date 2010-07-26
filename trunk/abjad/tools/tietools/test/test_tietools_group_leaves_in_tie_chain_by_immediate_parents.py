from abjad import *


def test_tietools_group_leaves_in_tie_chain_by_immediate_parents_01( ):
   '''Group leaves in tie chain by immediate parent.'''

   t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 2)
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

   parts = tietools.group_leaves_in_tie_chain_by_immediate_parents(t.leaves[0].tie.chain)
   
   assert len(parts) == 2
   assert parts[0] == list(t.leaves[:2])
   assert parts[1] == list(t.leaves[2:])


def test_tietools_group_leaves_in_tie_chain_by_immediate_parents_02( ):
   '''Group leaves in tie chain by immediate parent.'''

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

   parts = tietools.group_leaves_in_tie_chain_by_immediate_parents(t.leaves[0].tie.chain)
   
   assert len(parts) == 1
   assert parts[0] == list(t.leaves)


def test_tietools_group_leaves_in_tie_chain_by_immediate_parents_03( ):
   '''Group leaves in tie chain by immediate parent.'''

   t = Note(0, (1, 4))
   
   parts = tietools.group_leaves_in_tie_chain_by_immediate_parents(t.tie.chain)
   
   assert len(parts) == 1
   assert parts[0] == [t]
