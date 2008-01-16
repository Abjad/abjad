from abjad import *


### TODO - write some tests with nested containers ###


def test_leaf_numbering_01( ):
   t = Voice(Note(0, (1, 8)) * 15)
   for i, x in enumerate(t):
      assert x.number == i

def test_leaf_numbering_02( ):
   t = Staff(Note(0, (1, 8)) * 15)
   for i, x in enumerate(t):
      assert x.number == i

def test_leaf_numbering_03( ):
   t = Staff(Note(0, (1, 8)) * 15)
   t[10] = Rest((1, 8))
   for i, x in enumerate(t):
      assert x.number == i
 
def test_leaf_numbering_04( ):
   t = Staff(Note(0, (1, 8)) * 15)
   t[10 : 10] = [Rest((1, 8))]
   for i, x in enumerate(t):
      assert x.number == i
 
def test_leaf_numbering_05( ):
   t = Staff(Note(0, (1, 8)) * 15)
   t[10 : 12] = [Rest((1, 8))]
   for i, x in enumerate(t):
      assert x.number == i
