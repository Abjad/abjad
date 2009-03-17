from abjad import *


def test_offset_containers_01( ):
   '''context and score offsets works on sequential voices.'''
   t = Staff([Voice(run(4)), Voice(run(4))])
   for i, x in enumerate(t):
      assert x.offset.context == x.offset.score == i * Rational(4, 8)


def test_offset_containers_02( ):
   '''context and score offsets works on sequential staves.'''
   t = Sequential([Staff(run(4)), Staff(run(4))])
   for i, x in enumerate(t):
      assert x.offset.context == x.offset.score == i * Rational(4, 8)


def test_offset_containers_03( ):
   '''context and score offsets works on sequential staves.'''
   t = Sequential([Staff(run(4)), Staff(run(4))])
   for i, x in enumerate(t):
      assert x.offset.context == x.offset.score == i * Rational(4, 8)


def test_offset_containers_04( ):
   '''context and score offsets works on sequential staves.'''
   t = Voice(FixedDurationTuplet((1, 4), run(3)) * 3)
   assert t[0].offset.context == t[0].offset.score == 0
   assert t[1].offset.context == t[1].offset.score == Rational(1, 4)
   assert t[2].offset.context == t[2].offset.score == 2 * Rational(1, 4)


def test_offset_containers_05( ):
   '''context and score offsets work on tuplets between notes.'''
   tp = FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)
   t = Voice([Note(0, (1, 8)), tp, Note(0, (1, 8))])
   assert t[0].offset.context == t[0].offset.score == 0
   assert t[1].offset.context == t[1].offset.score == Rational(1, 8)
   assert t[2].offset.context == t[2].offset.score == Rational(3, 8)


def test_offset_containers_06( ):
   '''context and score offsets work on nested tuplets.'''
   tp = FixedDurationTuplet((1, 4), run(3))
   t = FixedDurationTuplet((2, 4), [Note(0, (1, 4)), tp, Note(0, (1, 4))])
   assert t[0].offset.context == t[0].offset.score == 0
   assert t[1].offset.context == t[1].offset.score == Rational(1, 6)
   assert t[2].offset.context == t[2].offset.score == Rational(2, 6)


### nested contexts ###

def test_offset_containers_10( ):
   '''context and score offsets work on nested contexts.'''
   v = Voice(run(4))
   t = Staff([Note(0, (1, 8)), v, Note(0, (1, 8))])
   assert t[0].offset.context == t[0].offset.score == 0
   assert t[1].offset.context == t[1].offset.score == Rational(1, 8)
   assert t[2].offset.context == t[2].offset.score == Rational(5, 8)
   

def test_offset_containers_12( ):
   '''context and score offsets work on nested parallel contexts.'''
   v1 = Voice(run(4))
   v2 = Voice(run(4))
   t = Staff([v1, v2])
   t.brackets = 'double-angle'
   assert t[0].offset.context == t[0].offset.score == 0
   assert t[1].offset.context == t[1].offset.score == 0


import py.test 
def test_offset_containers_13( ):
   '''offset on contexts works in nested parallel and sequential contexts.'''
   v1 = Voice(run(4))
   v2 = Voice(run(4))
   v3 = Voice(run(4))
   v1b= Voice(run(4))
   v2b= Voice(run(4))
   v3b= Voice(run(4))
   s1 = Staff([Parallel([v1, v2]), v3])
   s2 = Staff([Parallel([v1b, v2b]), v3b])
   gs = GrandStaff([s1, s2])
   assert v1.offset.context == v1.offset.score == 0
   assert v2.offset.context == v2.offset.score == 0
   assert v3.offset.context == v3.offset.score == Rational(4, 8)
   assert v1b.offset.context == v1b.offset.score == 0
   assert v2b.offset.context == v2b.offset.score == 0
   assert v3b.offset.context == Rational(4, 8)
   assert v3b.offset.context == v3b.offset.score == Rational(4, 8)
