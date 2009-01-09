from abjad import *


def test_context_offsets_01( ):
   v1 = Voice(Note(0, (1, 8)) * 15)
   v2 = Voice(Note(0, (1, 8)) * 15)
   t = Staff([v1, v2])
   for i, x in enumerate(t):
      assert x.offset.context == x.offset.score == i * Rational(15, 8)


### tuplets ###

def test_context_offset_05( ):
   tp = FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)
   t = Voice([Note(0, (1, 8)), tp, Note(0, (1, 8))])
   offset = 0
   for x, d in zip(t, [(1, 8), (3, 12)]):
      assert x.offset.context == x.offset.score == offset
      offset += Rational(*d)


def test_context_offset_06( ):
   '''Offset works on nested tuplets.'''
   tp = FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)
   t = FixedDurationTuplet((2, 4), [Note(0, (1, 4)), tp, Note(0, (1, 4))])
   offset = 0
   for x, d in zip(t, [(1, 6), (3, 18)]):
      assert x.offset.context == x.offset.score == offset
      offset += Rational(*d)


### nested contexts ###

def test_context_offset_10( ):
   '''offset on context works in nested contexts.'''
   v = Voice(Note(0, (1, 8)) * 4)
   t = Staff([Note(0, (1, 8)), v, Note(0, (1, 8))])
   offset = 0
   for x, d in zip(t, [(1, 8), (4, 8)]):
      assert x.offset.context == x.offset.score == offset
      offset += Rational(*d)
   

def test_context_offset_11( ):
   '''offset on contexts works in sequential contexts.'''
   v1 = Voice(Note(0, (1, 8)) * 4)
   v2 = Voice(Note(0, (1, 8)) * 4)
   v3 = Voice(Note(0, (1, 8)) * 4)
   t = Staff([v1, v2, v3])
   for i, x in enumerate(t):
      assert x.offset.context == x.offset.score == i * Rational(4, 8)


def test_context_offset_12( ):
   '''offset on contexts works in nested parallel contexts.'''
   v1 = Voice(Note(0, (1, 8)) * 4)
   v2 = Voice(Note(0, (1, 8)) * 4)
   t = Staff([v1, v2])
   t.brackets = 'double-angle'
   for x in t:
      assert x.offset.context == x.offset.score == 0


def test_context_offset_13( ):
   '''offset on contexts works in nested parallel and sequential contexts.'''
   v1 = Voice(Note(0, (1, 8)) * 4)
   v2 = Voice(Note(0, (1, 8)) * 4)
   v3 = Voice(Note(0, (1, 8)) * 4)
   v1b = Voice(Note(0, (1, 8)) * 4)
   v2b = Voice(Note(0, (1, 8)) * 4)
   v3b = Voice(Note(0, (1, 8)) * 4)
   s1 = Staff([Parallel([v1, v2]), v3])
   s2 = Staff([Parallel([v1b, v2b]), v3b])
   gs = GrandStaff([s1, s2])
   assert v1.offset.context == v1.offset.score == 0
   assert v2.offset.context == v2.offset.score == 0
   assert v3.offset.context == v3.offset.score == Rational(4, 8)
   assert v1b.offset.context == Rational(0, 8)
   assert v1b.offset.score == Rational(8, 8)
   assert v2b.offset.context == Rational(0, 8)
   assert v2b.offset.score == Rational(8, 8)
   assert v3b.offset.context == Rational(4, 8)
   assert v3b.offset.score == Rational(12, 8)
