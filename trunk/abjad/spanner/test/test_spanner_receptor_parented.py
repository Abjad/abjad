from abjad import *
import py.test


def test_spanner_receptor_parented_01( ):
   '''Leaves are parented when spanner is attached to them.'''

   t = Staff(run(4))
   b = Beam(t.leaves)

   assert not t.beam.parented
   for leaf in t.leaves:
      assert leaf.beam.parented


def test_spanner_receptor_parented_02( ):
   '''Leaves are parented when spanner is attached to their parent.'''

   t = Staff(run(4))
   b = Beam(t)

   assert t.beam.parented
   for leaf in t.leaves:
      assert leaf.beam.parented


def test_spanner_receptor_parented_03( ):
   '''Leaves and Containers are parented when spanner is attached to 
      their grandparent and parent repsectively.'''

   t = Staff(Voice(run(4)) * 2)

   assert py.test.raises(ContiguityError, 'b = Beam(t)')
#   assert t.beam.parented
#   for v in t:
#      assert v.beam.parented
#   for leaf in t.leaves:
#      assert leaf.beam.parented
