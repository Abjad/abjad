from abjad.helpers.is_containerized_tie_chain import _is_containerized_tie_chain
from abjad import *


def test_is_containerized_tie_chain_01( ):
   '''False for unincorporated components.'''

   t = run(4)
   Tie(t[:])

   assert not _is_containerized_tie_chain(t[0].tie.chain)


def test_is_containerized_tie_chain_02( ):
   t = Staff(run(4))
   Tie(t[:])

   assert _is_containerized_tie_chain(t[0].tie.chain)


def test_is_containerized_tie_chain_03( ):
   '''Measuring-crossing tie yields noncontiguous chain.'''

   t = Staff(RigidMeasure((2, 8), run(2)) * 2)
   Tie(t.leaves[1:3])

   r'''
   \new Staff {
         \time 2/8
         c'8
         c'8 ~
         \time 2/8
         c'8
         c'8
   }
   '''

   assert _is_containerized_tie_chain(t.leaves[0].tie.chain)
   assert not _is_containerized_tie_chain(t.leaves[1].tie.chain)
   assert not _is_containerized_tie_chain(t.leaves[2].tie.chain)
   assert _is_containerized_tie_chain(t.leaves[3].tie.chain)


def test_is_containerized_tie_chain_04( ):
   '''Tuplet-crossing tie yields noncontiguous chain.'''

   t = Staff(FixedDurationTuplet((2, 8), run(3)) * 2)
   Tie(t.leaves[2:4])

   r'''
   \new Staff {
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
   }
   '''

   assert _is_containerized_tie_chain(t.leaves[0].tie.chain)
   assert _is_containerized_tie_chain(t.leaves[1].tie.chain)
   assert not _is_containerized_tie_chain(t.leaves[2].tie.chain)
   assert not _is_containerized_tie_chain(t.leaves[3].tie.chain)
   assert _is_containerized_tie_chain(t.leaves[4].tie.chain)
   assert _is_containerized_tie_chain(t.leaves[5].tie.chain)
