from abjad import *


def test_offset_leaves_01( ):
   t = Voice(run(16))
   for i, x in enumerate(t):
      assert x.offset.context == x.offset.score == i * Rational(1, 8)


def test_offset_leaves_02( ):
   t = Staff(run(16))
   for i, x in enumerate(t):
      assert x.offset.context == x.offset.score == i * Rational(1, 8)


def test_offset_leaves_03( ):
   t = Staff(run(16))
   t[10] = Rest((1, 8))
   for i, x in enumerate(t):
      assert x.offset.context == x.offset.score == i * Rational(1, 8)
 

def test_offset_leaves_04( ):
   t = Staff(run(16))
   t[10 : 10] = [Rest((1, 8))]
   for i, x in enumerate(t):
      assert x.offset.context == x.offset.score == i * Rational(1, 8)
 

def test_offset_leaves_05( ):
   t = Staff(run(16))
   t[10 : 12] = [Rest((1, 8))]
   for i, x in enumerate(t):
      assert x.offset.context == x.offset.score == i * Rational(1, 8)


def test_offset_leaves_06( ):
   '''Offset works with sequential structures.'''
   v1 = Voice(run(16))
   v2 = Voice(Note(4, (1, 8)) * 15)
   t = Parallel([v1, v2])
   for i, x in enumerate(v1):
      assert x.offset.context == x.offset.score == i * Rational(1, 8)
   for i, x in enumerate(v2):
      assert x.offset.context == x.offset.score == i * Rational(1, 8)


### tuplets ###

def test_offset_leaves_10( ):
   t = FixedDurationTuplet((1,4), run(3))
   for i, x in enumerate(t):
      assert x.offset.context == x.offset.score == i * Rational(1, 12)


def test_offset_leaves_11( ):
   tp = FixedDurationTuplet((1, 4), run(3))
   t = Voice([Note(0, (1, 8)), tp, Note(0, (1, 8))])
   offset = 0
   for x, d in zip(t.leaves, [(1, 8), (1, 12), (1, 12), (1, 12), (1, 8)]):
      assert x.offset.context == x.offset.score == offset
      offset += Rational(*d)


def test_offset_leaves_12( ):
   '''Offset works on nested tuplets.'''
   tp = FixedDurationTuplet((1, 4), run(3))
   t = FixedDurationTuplet((2, 4), [Note(0, (1, 4)), tp, Note(0, (1, 4))])
   offset = 0
   for x, d in zip(t.leaves, [(1, 6), (1, 18), (1, 18), (1, 18), (1, 6)]):
      assert x.offset.context == x.offset.score == offset
      offset += Rational(*d)


## parallel ##

def test_offset_leaves_13( ):
   '''Offset works with parallel structures.'''
   v1 = Voice(run(16))
   v2 = Voice(run(16))
   t = Staff([v1, v2])
   t.brackets = 'double-angle'
   for i, x in enumerate(v1):
      assert x.offset.context == x.offset.score == i * Rational(1, 8)
   for i, x in enumerate(v2):
      assert x.offset.context == x.offset.score == i * Rational(1, 8)


## nested contexts ##

def test_offset_leaves_14( ):
   '''offset on leaves works in nested contexts.'''
   v = Voice(run(4))
   t = Staff([Note(0, (1, 8)), v, Note(0, (1, 8))])
   for i, x in enumerate(t.leaves):
      assert x.offset.score == i * Rational(1, 8)
   for i, x in enumerate(v.leaves):
      assert x.offset.context == i * Rational(1, 8) 
      assert x.offset.score == i * Rational(1, 8) + Rational(1, 8)
   
   
def test_offset_leaves_15( ):
   '''offset on leaves works in sequential contexts.'''
   v1 = Voice(run(4))
   v2 = Voice(run(4))
   t = Staff([v1, v2])
   for i, x in enumerate(v1.leaves):
      assert x.offset.context == x.offset.score == i * Rational(1, 8)
   for i, x in enumerate(v2.leaves):
      assert x.offset.context  == i * Rational(1, 8)
      assert x.offset.score  == i * Rational(1, 8) + Rational(1, 2)


def test_offset_leaves_16( ):
   '''offset on leaves works in nested parallel contexts.'''
   v1 = Voice(run(4))
   v2 = Voice(run(4))
   t = Staff([v1, v2])
   t.brackets = 'double-angle'
   for i, x in enumerate(v1.leaves):
      assert x.offset.context == x.offset.score == i * Rational(1, 8)
   for i, x in enumerate(v2.leaves):
      assert x.offset.context == x.offset.score == i * Rational(1, 8)


def test_offset_leaves_17( ):
   '''offset on leaves works in nested parallel and sequential contexts.'''
   v1 = Voice(run(4))
   v2 = Voice(run(4))
   v3 = Voice(run(4))
   t = Staff([Parallel([v1, v2]), v3])
   for i, x in enumerate(v3.leaves):
      assert x.offset.context == i * Rational(1, 8)
      assert x.offset.score == i * Rational(1, 8) + Rational(4, 8)


def test_offset_leaves_18( ):
   '''offset on leaves works in nested parallel and sequential contexts.'''
   v1 = Voice(run(4))
   v2 = Voice(run(4))
   v3 = Voice(run(4))
   t = Staff([v3, Parallel([v1, v2])])
   for i, x in enumerate(v1.leaves):
      assert x.offset.context == i * Rational(1, 8)
      assert x.offset.score == i * Rational(1, 8) + Rational(4, 8)
   for i, x in enumerate(v2.leaves):
      assert x.offset.context == i * Rational(1, 8)
      assert x.offset.score == i * Rational(1, 8) + Rational(4, 8)
