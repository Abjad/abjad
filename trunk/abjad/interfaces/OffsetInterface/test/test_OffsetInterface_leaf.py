from abjad import *


def test_OffsetInterface_leaf_01( ):
   t = Voice(leaftools.make_repeated_notes(16))
   for i, x in enumerate(t):
      assert x.offset.prolated.start == i * Rational(1, 8)


def test_OffsetInterface_leaf_02( ):
   t = Staff(leaftools.make_repeated_notes(16))
   for i, x in enumerate(t):
      assert x.offset.prolated.start == i * Rational(1, 8)


def test_OffsetInterface_leaf_03( ):
   t = Staff(leaftools.make_repeated_notes(16))
   t[10] = Rest((1, 8))
   for i, x in enumerate(t):
      assert x.offset.prolated.start == i * Rational(1, 8)
 

def test_OffsetInterface_leaf_04( ):
   t = Staff(leaftools.make_repeated_notes(16))
   t[10 : 10] = [Rest((1, 8))]
   for i, x in enumerate(t):
      assert x.offset.prolated.start == i * Rational(1, 8)
 

def test_OffsetInterface_leaf_05( ):
   t = Staff(leaftools.make_repeated_notes(16))
   t[10 : 12] = [Rest((1, 8))]
   for i, x in enumerate(t):
      assert x.offset.prolated.start == i * Rational(1, 8)


def test_OffsetInterface_leaf_06( ):
   '''Offset works with explicit voice threads.'''
   v1 = Voice(leaftools.make_repeated_notes(16))
   v2 = Voice(leaftools.make_repeated_notes(16))
   v1.name = v2.name = 'voice'
   t = Container([v1, v2])
   for i, x in enumerate(t.leaves):
      assert x.offset.prolated.start == i * Rational(1, 8)


def test_OffsetInterface_leaf_07( ):
   t = FixedDurationTuplet((1,4), leaftools.make_repeated_notes(3))
   for i, x in enumerate(t):
      assert x.offset.prolated.start == i * Rational(1, 12)


def test_OffsetInterface_leaf_08( ):
   tp = FixedDurationTuplet((1, 4), leaftools.make_repeated_notes(3))
   t = Voice([Note(0, (1, 8)), tp, Note(0, (1, 8))])
   offset = 0
   for x, d in zip(t.leaves, [(1, 8), (1, 12), (1, 12), (1, 12), (1, 8)]):
      assert x.offset.prolated.start == offset
      offset += Rational(*d)


def test_OffsetInterface_leaf_09( ):
   '''Offset works on nested tuplets.'''
   tp = FixedDurationTuplet((1, 4), leaftools.make_repeated_notes(3))
   t = FixedDurationTuplet((2, 4), [Note(0, (1, 4)), tp, Note(0, (1, 4))])
   offset = 0
   for x, d in zip(t.leaves, [(1, 6), (1, 18), (1, 18), (1, 18), (1, 6)]):
      assert x.offset.prolated.start == offset
      offset += Rational(*d)


## parallel ##

def test_OffsetInterface_leaf_10( ):
   '''Offset works with parallel structures.'''
   v1 = Voice(leaftools.make_repeated_notes(16))
   v2 = Voice(leaftools.make_repeated_notes(16))
   t = Staff([v1, v2])
   t.parallel = True
   for i, x in enumerate(v1):
      assert x.offset.prolated.start == i * Rational(1, 8)
   for i, x in enumerate(v2):
      assert x.offset.prolated.start == i * Rational(1, 8)


## nested contexts ##

def test_OffsetInterface_leaf_11( ):
   '''offset on leaves works in nested contexts.'''
   v = Voice(leaftools.make_repeated_notes(4))
   t = Staff([Note(0, (1, 8)), v, Note(0, (1, 8))])
   for i, x in enumerate(t.leaves):
      assert x.offset.prolated.start == i * Rational(1, 8)
   for i, x in enumerate(v.leaves):
      assert x.offset.prolated.start == i * Rational(1, 8) + Rational(1, 8)
   
   
def test_OffsetInterface_leaf_12( ):
   '''offset on leaves works in sequential contexts.'''
   v1 = Voice(leaftools.make_repeated_notes(4))
   v2 = Voice(leaftools.make_repeated_notes(4))
   t = Staff([v1, v2])
   for i, x in enumerate(v1.leaves):
      assert x.offset.prolated.start == i * Rational(1, 8)
   for i, x in enumerate(v2.leaves):
      assert x.offset.prolated.start  == i * Rational(1, 8) + Rational(1, 2)


def test_OffsetInterface_leaf_13( ):
   '''offset on leaves works in nested parallel contexts.'''
   v1 = Voice(leaftools.make_repeated_notes(4))
   v2 = Voice(leaftools.make_repeated_notes(4))
   t = Staff([v1, v2])
   t.parallel = True
   for i, x in enumerate(v1.leaves):
      assert x.offset.prolated.start == i * Rational(1, 8)
   for i, x in enumerate(v2.leaves):
      assert x.offset.prolated.start == i * Rational(1, 8)


def test_OffsetInterface_leaf_14( ):
   '''offset on leaves works in nested parallel and sequential contexts.'''
   v1 = Voice(leaftools.make_repeated_notes(4))
   v2 = Voice(leaftools.make_repeated_notes(4))
   v3 = Voice(leaftools.make_repeated_notes(4))
   t = Staff([Container([v1, v2]), v3])
   t[0].parallel = True
   for i, x in enumerate(v3.leaves):
      assert x.offset.prolated.start == i * Rational(1, 8) + Rational(4, 8)


def test_OffsetInterface_leaf_15( ):
   '''offset on leaves works in nested parallel and sequential contexts.'''
   v1 = Voice(leaftools.make_repeated_notes(4))
   v2 = Voice(leaftools.make_repeated_notes(4))
   v3 = Voice(leaftools.make_repeated_notes(4))
   t = Staff([v3, Container([v1, v2])])
   t[1].parallel = True
   for i, x in enumerate(v1.leaves):
      assert x.offset.prolated.start == i * Rational(1, 8) + Rational(4, 8)
   for i, x in enumerate(v2.leaves):
      assert x.offset.prolated.start == i * Rational(1, 8) + Rational(4, 8)
