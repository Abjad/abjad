from abjad import *
from py.test import raises


def test_staff_append_01( ):
   '''Append one note.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t.append(Note(0, (1, 4)))
   assert check(t)
   assert len(t) == 5
   assert t.duration.contents == Rational(5, 4)


def test_staff_append_02( ):
   '''Append one chord.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t.append(Chord([2, 3, 4], (1, 4)))
   assert check(t)
   assert len(t) == 5
   assert t.duration.contents == Rational(5, 4)


def test_staff_append_03( ):
   '''Append one tuplet.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t.append(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3))
   assert check(t)
   assert len(t) == 5
   assert t.duration.contents == Rational(5, 4)


def test_staff_append_04( ):
   '''Empty containers are allowed but not well-formed.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t.append(FixedDurationTuplet((2, 8), [ ]))
   assert len(t) == 5
   assert t.duration.contents == Rational(5, 4)
