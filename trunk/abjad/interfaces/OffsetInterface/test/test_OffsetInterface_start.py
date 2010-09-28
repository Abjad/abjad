from abjad import *
import py.test


def test_OffsetInterface_start_01( ):
   '''Prolated offsets works on threaded sequential voices.'''
   t = Staff([Voice(notetools.make_repeated_notes(4)), Voice(notetools.make_repeated_notes(4))])
   t[0].name = t[1].name = 'voice'
   for i, x in enumerate(t):
      assert x.offset.start == i * Fraction(4, 8)


def test_OffsetInterface_start_02( ):
   '''Prolated offset does NOT go across sequential staves.'''
   t = Container([Staff(notetools.make_repeated_notes(4)), Staff(notetools.make_repeated_notes(4))])
   t[0].name = t[1].name = 'staff'
   assert t[0].offset.start == Fraction(0)
   assert t[1].offset.start == Fraction(1, 2)


def test_OffsetInterface_start_03( ):
   '''Prolated offsets follows strict threads.'''
   t = Staff([Voice(notetools.make_repeated_notes(4)), Voice(notetools.make_repeated_notes(4))])
   for i, x in enumerate(t):
      assert x.offset.start == i * Fraction(4, 8)


def test_OffsetInterface_start_04( ):
   '''Prolated offsets works on sequential tuplets.'''
   t = Voice(tuplettools.FixedDurationTuplet((1, 4), notetools.make_repeated_notes(3)) * 3)
   assert t[0].offset.start == 0
   assert t[1].offset.start == Fraction(1, 4)
   assert t[2].offset.start == 2 * Fraction(1, 4)


def test_OffsetInterface_start_05( ):
   '''Prolated offsets work on tuplets between notes.'''
   tp = tuplettools.FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)
   t = Voice([Note(0, (1, 8)), tp, Note(0, (1, 8))])
   assert t[0].offset.start == 0
   assert t[1].offset.start == Fraction(1, 8)
   assert t[2].offset.start == Fraction(3, 8)


def test_OffsetInterface_start_06( ):
   '''Prolated offsets work on nested tuplets.'''
   tp = tuplettools.FixedDurationTuplet((1, 4), notetools.make_repeated_notes(3))
   t = tuplettools.FixedDurationTuplet((2, 4), [Note(0, (1, 4)), tp, Note(0, (1, 4))])
   assert t[0].offset.start == 0
   assert t[1].offset.start == Fraction(1, 6)
   assert t[2].offset.start == Fraction(2, 6)


## nested contexts ##

def test_OffsetInterface_start_07( ):
   '''Prolated offsets work on nested contexts.'''
   vin = Voice(notetools.make_repeated_notes(4))
   vout = Voice([Note(0, (1, 8)), vin])
   vin.name = vout.name = 'voice'
   t = Staff([Note(1, (1, 8)), vout])
   assert vin.offset.start == Fraction(2, 8)
   assert vout.offset.start == Fraction(1, 8)
   

def test_OffsetInterface_start_08( ):
   '''Prolated offsets work on nested parallel contexts.'''
   v1 = Voice(notetools.make_repeated_notes(4))
   v2 = Voice(notetools.make_repeated_notes(4))
   t = Staff([v1, v2])
   t.parallel = True
   assert t[0].offset.start == 0
   assert t[1].offset.start == 0


def test_OffsetInterface_start_09( ):
   '''Prolated offsets works in nested parallel and sequential 
   contexts.'''
   v1 = Voice(notetools.make_repeated_notes(4))
   v2 = Voice(notetools.make_repeated_notes(4))
   v1b= Voice(notetools.make_repeated_notes(4))
   v2b= Voice(notetools.make_repeated_notes(4))
   v1.name = v1b.name = 'voiceOne'
   s1 = Staff([v1, v1b])
   s2 = Staff([v2, v2b])
   gs = scoretools.GrandStaff([s1, s2])
   assert v1.offset.start == 0
   assert v2.offset.start == 0
   assert v1b.offset.start == Fraction(4, 8)
   assert v2b.offset.start == Fraction(4, 8)
