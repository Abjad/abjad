from abjad import *
from py.test import raises


def test_staff_setitem_01( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t)
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Rest)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], Skip)
   assert isinstance(t[4], FixedDurationTuplet)
   t[1] = Chord([12, 13, 15], (1, 4))
   assert len(t) == 5
   assert check(t)
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], Skip)
   assert isinstance(t[4], FixedDurationTuplet)
   t[0] = Rest((1, 4))
   assert len(t) == 5
   assert check(t)
   assert isinstance(t[0], Rest)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], Skip)
   assert isinstance(t[4], FixedDurationTuplet)
   t[-2] = FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   assert len(t) == 5
   assert check(t)
   assert isinstance(t[0], Rest)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], FixedDurationTuplet)
   assert isinstance(t[4], FixedDurationTuplet)
   t[-1] = Note(13, (1, 4))
   assert len(t) == 5
   assert check(t)
   assert isinstance(t[0], Rest)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], FixedDurationTuplet)
   assert isinstance(t[4], Note)
   t[-3] = Skip((1, 4))
   assert len(t) == 5
   assert check(t)
   assert isinstance(t[0], Rest)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Skip)
   assert isinstance(t[3], FixedDurationTuplet)
   assert isinstance(t[4], Note)


def test_staff_setitem_02( ):
   '''Reassign the *entire* contents of t.'''
   t = Staff(Note(0, (1, 4)) * 4)
   assert t.duration.contents == Rational(4, 4)
   t[ : ] = Note(0, (1, 8)) * 4
   assert t.duration.contents == Rational(4, 8)


def test_staff_setitem_03( ):
   '''Item-assign an empty container to t.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t[0] = Voice([ ])


def test_staff_setitem_04( ):
   '''Slice-assign empty containers to t.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t[0 : 2] = [Voice([ ]), Voice([ ])]


def test_staff_setitem_05( ):
   '''Bark when user assigns a slice to an item.'''
   t = Staff(Note(0, (1, 4)) * 4)
   assert raises(TypeError, 't[0] = [Note(2, (1, 4)), Note(2, (1, 4))]')


def test_staff_setitem_06( ):
   '''Bark when user assigns an item to a slice.'''
   t = Staff(Note(0, (1, 4)) * 4)
   assert raises(TypeError, 't[0:2] = Note(2, (1, 4))')


def test_staff_setitem_07( ):
   '''Slice-assign notes.'''
   t = Staff(Note(0, (1, 8)) * 8)
   t[0 : 4] = Note(2, (1, 8)) * 4
   assert len(t) == 8
   for x in t[0 : 4]:
      assert x.pitch.number == 2
   for x in t[4 : 8]:
      assert x.pitch.number == 0
   assert check(t)


def test_staff_setitem_08( ):
   '''Slice-assign chords.'''
   t = Staff(Note(0, (1, 8)) * 8)
   t[0 : 4] = Chord([2, 3, 4], (1, 4)) * 4
   assert len(t) == 8
   for x in t[0 : 4]:
      assert x.duration.written == Rational(1, 4)
   for x in t[4 : 8]:
      assert x.duration.written == Rational(1, 8)
   assert check(t)


def test_staff_setitem_09( ):
   '''Slice-assign tuplets.'''
   t = Staff(Note(0, (1, 8)) * 8)
   t[0 : 4] = FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 2
   assert len(t) == 6
   for i, x in enumerate(t):
      if i in [0, 1]:
         assert isinstance(x, FixedDurationTuplet)
      else:
         assert isinstance(x, Note)
   assert check(t)


def test_staff_setitem_10( ):
   '''Slice-assign measures.'''
   t = Staff(Note(0, (1, 8)) * 8)
   t[0 : 4] = RigidMeasure((2, 8), Note(0, (1, 8)) * 2) * 2
   assert len(t) == 6
   for i, x in enumerate(t):
      if i in [0, 1]:
         assert isinstance(x, RigidMeasure)
      else:
         assert isinstance(x, Note)
   assert check(t)
