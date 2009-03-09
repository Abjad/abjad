from abjad import *


### TODO - write some tests with nested containers ###

def test_leaf_numbering_leaf_01( ):
   t = Voice(run(15))
   for i, leaf in enumerate(t):
      assert leaf.numbering.leaf == i


def test_leaf_numbering_leaf_02( ):
   t = Staff(run(15))
   for i, leaf in enumerate(t):
      assert leaf.numbering.leaf == i


def test_leaf_numbering_leaf_03( ):
   t = Staff(run(15))
   t[10] = Rest((1, 8))
   for i, leaf in enumerate(t):
      assert leaf.numbering.leaf == i
 

def test_leaf_numbering_leaf_04( ):
   t = Staff(run(15))
   t[10:10] = [Rest((1, 8))]
   for i, leaf in enumerate(t):
      assert leaf.numbering.leaf == i
 

def test_leaf_numbering_leaf_05( ):
   t = Staff(run(15))
   t[10:12] = [Rest((1, 8))]
   for i, leaf in enumerate(t):
      assert leaf.numbering.leaf == i
