from abjad import *


def test_offset_containers_01( ):
   '''thread and score offsets works on threaded sequential voices.'''
   t = Staff([Voice(run(4)), Voice(run(4))])
   t[0].name = t[1].name = 'voice'
   for i, x in enumerate(t):
      assert x.offset.thread == x.offset.score == i * Rational(4, 8)


def test_offset_containers_02( ):
   '''thread offsets does NOT go across sequential staves.'''
   t = Container([Staff(run(4)), Staff(run(4))])
   t[0].name = t[1].name = 'staff'
   assert t[0].offset.thread == Rational(0)
   assert t[1].offset.thread == Rational(0)
   assert t[0].offset.score == Rational(0)
   assert t[1].offset.score == Rational(1, 2)


def test_offset_containers_03( ):
   '''thread offsets follows strict threads.'''
   t = Staff([Voice(run(4)), Voice(run(4))])
   assert t[0].offset.thread == 0
   assert t[1].offset.thread == 0
   for i, x in enumerate(t):
      assert x.offset.score == i * Rational(4, 8)


def test_offset_containers_04( ):
   '''thread and score offsets works on sequential tuplets.'''
   t = Voice(FixedDurationTuplet((1, 4), run(3)) * 3)
   assert t[0].offset.thread == t[0].offset.score == 0
   assert t[1].offset.thread == t[1].offset.score == Rational(1, 4)
   assert t[2].offset.thread == t[2].offset.score == 2 * Rational(1, 4)


def test_offset_containers_05( ):
   '''thread and score offsets work on tuplets between notes.'''
   tp = FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)
   t = Voice([Note(0, (1, 8)), tp, Note(0, (1, 8))])
   assert t[0].offset.thread == t[0].offset.score == 0
   assert t[1].offset.thread == t[1].offset.score == Rational(1, 8)
   assert t[2].offset.thread == t[2].offset.score == Rational(3, 8)


def test_offset_containers_06( ):
   '''thread and score offsets work on nested tuplets.'''
   tp = FixedDurationTuplet((1, 4), run(3))
   t = FixedDurationTuplet((2, 4), [Note(0, (1, 4)), tp, Note(0, (1, 4))])
   assert t[0].offset.thread == t[0].offset.score == 0
   assert t[1].offset.thread == t[1].offset.score == Rational(1, 6)
   assert t[2].offset.thread == t[2].offset.score == Rational(2, 6)


### nested contexts ###

def test_offset_containers_10( ):
   '''thread and score offsets work on nested contexts.'''
   vin = Voice(run(4))
   vout = Voice([Note(0, (1, 8)), vin])
   vin.name = vout.name = 'voice'
   t = Staff([Note(1, (1, 8)), vout])
   assert vin.offset.thread == Rational(1, 8)
   assert vin.offset.score == Rational(2, 8)
   assert vout.offset.thread == 0
   assert vout.offset.score == Rational(1, 8)
   

def test_offset_containers_12( ):
   '''thread and score offsets work on nested parallel contexts.'''
   v1 = Voice(run(4))
   v2 = Voice(run(4))
   t = Staff([v1, v2])
   t.parallel = True
   assert t[0].offset.thread == t[0].offset.score == 0
   assert t[1].offset.thread == t[1].offset.score == 0


def test_offset_containers_13( ):
   '''threads and score offsets works in nested parallel and sequential 
   contexts.'''
   v1 = Voice(run(4))
   v2 = Voice(run(4))
   v1b= Voice(run(4))
   v2b= Voice(run(4))
   v1.name = v1b.name = 'voiceOne'
   s1 = Staff([v1, v1b])
   s2 = Staff([v2, v2b])
   gs = GrandStaff([s1, s2])
   assert v1.offset.thread == v1.offset.score == 0
   assert v2.offset.thread == v2.offset.score == 0
   assert v1b.offset.thread == v1b.offset.score == Rational(4, 8)
   assert v2b.offset.thread == 0
   assert v2b.offset.score == Rational(4, 8)
