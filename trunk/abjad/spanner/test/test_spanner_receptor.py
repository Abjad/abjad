from abjad import *

def test_spanner_receptor_spannedAbove_01( ):
   '''
   Leaves are spannedAbove when spanner is attached to them.
   '''
   t = Staff(run(4))
   b = Beam(t.leaves)
   assert not t.beam.spannedAbove
   for leaf in t.leaves:
      assert leaf.beam.spannedAbove


def test_spanner_receptor_spannedAbove_02( ):
   '''
   Leaves are spannedAbove when spanner is attached to their parent.
   '''
   t = Staff(run(4))
   b = Beam(t)
   assert t.beam.spannedAbove
   for leaf in t.leaves:
      assert leaf.beam.spannedAbove


def test_spanner_receptor_spannedAbove_03( ):
   '''
   Leaves and Containers are spannedAbove when spanner is attached to 
   their grandparent and parent repsectively.
   '''
   t = Staff(Voice(run(4)) * 2)
   b = Beam(t)
   assert t.beam.spannedAbove
   for v in t:
      assert v.beam.spannedAbove
   for leaf in t.leaves:
      assert leaf.beam.spannedAbove


