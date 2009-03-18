from abjad.helpers.is_tie_chain_in_same_parent import _is_tie_chain_in_same_parent
from abjad import *


def test_is_tie_chain_in_same_parent_01( ):
   '''False for unincorporated components.'''

   t = run(4)
   Tie(t[:])

   assert _is_tie_chain_in_same_parent(t[0].tie.chain)


def test_is_tie_chain_in_same_parent_02( ):
   '''True for tie chain with all leaves in same staff.'''

   t = Staff(run(4))
   Tie(t[:])

   assert _is_tie_chain_in_same_parent(t[0].tie.chain)


def test_is_tie_chain_in_same_parent_03( ):
   '''False for measure-crossing tie chain.'''

   t = Staff(RigidMeasure((2, 8), run(2)) * 2)
   Tie(t.leaves[1:3])

   r'''\new Staff {
         \time 2/8
         c'8
         c'8 ~
         \time 2/8
         c'8
         c'8
   }'''

   assert _is_tie_chain_in_same_parent(t.leaves[0].tie.chain)
   assert not _is_tie_chain_in_same_parent(t.leaves[1].tie.chain)
   assert not _is_tie_chain_in_same_parent(t.leaves[2].tie.chain)
   assert _is_tie_chain_in_same_parent(t.leaves[3].tie.chain)


def test_is_tie_chain_in_same_parent_04( ):
   '''False for tuplet-crossing tie chain.'''

   t = Staff(FixedDurationTuplet((2, 8), run(3)) * 2)
   Tie(t.leaves[2:4])

   r'''\new Staff {
      \times 2/3 {
         c'8
         c'8
         c'8 ~
      }
      \times 2/3 {
         c'8
         c'8
         c'8
      }
   }'''

   assert _is_tie_chain_in_same_parent(t.leaves[0].tie.chain)
   assert _is_tie_chain_in_same_parent(t.leaves[1].tie.chain)
   assert not _is_tie_chain_in_same_parent(t.leaves[2].tie.chain)
   assert not _is_tie_chain_in_same_parent(t.leaves[3].tie.chain)
   assert _is_tie_chain_in_same_parent(t.leaves[4].tie.chain)
   assert _is_tie_chain_in_same_parent(t.leaves[5].tie.chain)
