from abjad import *


### TODO - write some tests with tuplets ###

def test_leaf_offsets_01( ):
   t = Voice(Note(0, (1, 8)) * 15)
   for i, x in enumerate(t):
      assert x.offset == i * Rational(1, 8)

def test_leaf_offsets_02( ):
   t = Staff(Note(0, (1, 8)) * 15)
   for i, x in enumerate(t):
      assert x.offset == i * Rational(1, 8)

def test_leaf_offsets_03( ):
   t = Staff(Note(0, (1, 8)) * 15)
   t[10] = Rest((1, 8))
   for i, x in enumerate(t):
      assert x.offset == i * Rational(1, 8)
 
def test_leaf_offsets_04( ):
   t = Staff(Note(0, (1, 8)) * 15)
   t[10 : 10] = [Rest((1, 8))]
   for i, x in enumerate(t):
      assert x.offset == i * Rational(1, 8)
 
def test_leaf_offsets_05( ):
   t = Staff(Note(0, (1, 8)) * 15)
   t[10 : 12] = [Rest((1, 8))]
   for i, x in enumerate(t):
      assert x.offset == i * Rational(1, 8)
