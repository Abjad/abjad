from abjad import *


def test_staff_getitem_01( ):
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
   assert isinstance(t[-5], Note)
   assert isinstance(t[-4], Rest)
   assert isinstance(t[-3], Chord)
   assert isinstance(t[-2], Skip)
   assert isinstance(t[-1], FixedDurationTuplet)


def test_staff_getitem_02( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t)
   slice = t[0 : 0]
   assert len(slice) == 0
   assert check(t)


def test_staff_getitem_03( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t)
   slice = t[0 : 1]
   assert len(slice) == 1
   assert isinstance(slice[0], Note)
   for x in t:
      assert x.parentage.parent == t
   assert check(t)


def test_staff_getitem_04( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t)
   slice = t[-1 : ]
   assert len(slice) == 1
   assert isinstance(slice[0], FixedDurationTuplet)
   for x in slice:
      assert x.parentage.parent == t
   assert check(t)


def test_staff_getitem_05( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t)
   slice = t[1 : -1]
   assert len(slice) == 3
   assert isinstance(slice[0], Rest)
   assert isinstance(slice[1], Chord)
   assert isinstance(slice[2], Skip)
   for x in slice:
      assert x.parentage.parent == t
   assert check(t)


def test_staff_getitem_06( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t)
   slice = t[2 : ]
   assert len(slice) == 3
   assert isinstance(slice[0], Chord)
   assert isinstance(slice[1], Skip)
   assert isinstance(slice[2], FixedDurationTuplet)
   for x in slice:
      assert x.parentage.parent == t
   assert check(t)


def test_staff_getitem_07( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t)
   slice = t[ : -2]
   assert len(slice) == 3
   assert isinstance(slice[0], Note)
   assert isinstance(slice[1], Rest)
   assert isinstance(slice[2], Chord)
   for x in slice:
      assert x.parentage.parent == t
   assert check(t)


def test_staff_getitem_08( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t)
   slice = t[ : ]
   assert len(slice) == 5
   assert isinstance(slice, list)
   assert isinstance(slice[0], Note)
   assert isinstance(slice[1], Rest)
   assert isinstance(slice[2], Chord)
   assert isinstance(slice[3], Skip)
   assert isinstance(slice[4], FixedDurationTuplet)
   for x in slice:
      assert x.parentage.parent == t
   assert check(t)
