from abjad import *


def test_numbering_leaf_01( ):
   '''Leaves in staff number correctly.'''

   t = Staff(construct.scale(3))
   assert t[0].numbering.leaf == 0
   assert t[1].numbering.leaf == 1
   assert t[2].numbering.leaf == 2


def test_numbering_leaf_02( ):
   '''Leaves in measure in staff number correctly.'''

   t = Staff([RigidMeasure((3, 8), construct.scale(3))])
   leaves = t.leaves
   assert leaves[0].numbering.leaf == 0
   assert leaves[1].numbering.leaf == 1
   assert leaves[2].numbering.leaf == 2


def test_numbering_leaf_03( ):
   '''Leaves in multiple measures in staff number corretly.'''

   t = Staff(RigidMeasure((2, 8), construct.scale(2)) * 3)
   leaves = t.leaves
   assert leaves[0].numbering.leaf == 0
   assert leaves[1].numbering.leaf == 1
   assert leaves[2].numbering.leaf == 2
   assert leaves[3].numbering.leaf == 3
   assert leaves[4].numbering.leaf == 4
   assert leaves[5].numbering.leaf == 5


def test_numbering_leaf_04( ):
   '''Orphan leaves number correctly.'''

   t = Note(0, (1, 4))
   assert t.numbering.leaf == 0
