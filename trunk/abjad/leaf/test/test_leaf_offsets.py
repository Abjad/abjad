from abjad import *



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


### TUPLETS ###

def test_leaf_offset_06( ):
   t = FixedDurationTuplet((1,4), Note(0, (1, 8)) * 3)
   for i, x in enumerate(t):
      assert x.offset == i * Rational(1, 12)

def test_leaf_offset_07( ):
   tp = FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)
   t = Voice([Note(0, (1, 8)), tp, Note(0, (1, 8))])
   offset = 0
   for x, d in zip(t.leaves, [(1, 8), (1, 12), (1, 12), (1, 12), (1, 8)]):
      assert x.offset == offset
      offset += Rational(*d)

def test_leaf_offset_08( ):
   '''Offset works on nested tuplets.'''
   tp = FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)
   t = FixedDurationTuplet((2, 4), [Note(0, (1, 4)), tp, Note(0, (1, 4))])
   offset = 0
   for x, d in zip(t.leaves, [(1, 6), (1, 18), (1, 18), (1, 18), (1, 6)]):
      assert x.offset == offset
      offset += Rational(*d)


### PARALLEL ###

def test_leaf_offsets_10( ):
   '''Offset works with parallel structures.'''
   v1 = Voice(Note(0, (1, 8)) * 15)
   v2 = Voice(Note(4, (1, 8)) * 15)
   t = Parallel([v1, v2])
   for i, x in enumerate(v1):
      assert x.offset == i * Rational(1, 8)
   for i, x in enumerate(v2):
      assert x.offset == i * Rational(1, 8)

def test_leaf_offsets_11( ):
   '''Offset works with parallel structures.'''
   v1 = Voice(Note(0, (1, 8)) * 15)
   v2 = Voice(Note(4, (1, 8)) * 15)
   t = Staff([v1, v2])
   t.brackets = 'double-angle'
   for i, x in enumerate(v1):
      assert x.offset == i * Rational(1, 8)
   for i, x in enumerate(v2):
      assert x.offset == i * Rational(1, 8)

