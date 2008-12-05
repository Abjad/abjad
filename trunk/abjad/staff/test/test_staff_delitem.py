from abjad import *
from py.test import raises


def test_staff_delitem_01( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Rest)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], Skip)
   assert isinstance(t[4], FixedDurationTuplet)
   del(t[0])
   assert len(t) == 4
   assert isinstance(t[0], Rest)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Skip)
   assert isinstance(t[3], FixedDurationTuplet)
   del(t[0])
   assert len(t) == 3
   assert isinstance(t[0], Chord)
   assert isinstance(t[1], Skip)
   assert isinstance(t[2], FixedDurationTuplet)
   del(t[0])
   assert len(t) == 2
   assert isinstance(t[0], Skip)
   assert isinstance(t[1], FixedDurationTuplet)
   del(t[0])
   assert len(t) == 1
   assert isinstance(t[0], FixedDurationTuplet)
   del(t[0])
   assert len(t) == 0 


def test_staff_delitem_02( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Rest)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], Skip)
   assert isinstance(t[4], FixedDurationTuplet)
   del(t[-1])
   assert len(t) == 4
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Rest)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], Skip)
   del(t[-1])
   assert len(t) == 3
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Rest)
   assert isinstance(t[2], Chord)
   del(t[-1])
   assert len(t) == 2
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Rest)
   del(t[-1])
   assert len(t) == 1
   assert isinstance(t[0], Note)
   del(t[-1])
   assert len(t) == 0 


def test_staff_delitem_03( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Rest)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], Skip)
   assert isinstance(t[4], FixedDurationTuplet)
   del(t[3])
   assert len(t) == 4
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Rest)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], FixedDurationTuplet)
   del(t[-2])
   assert len(t) == 3
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Rest)
   assert isinstance(t[2], FixedDurationTuplet)
   del(t[2])
   assert len(t) == 2
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Rest)
   del(t[0])
   assert len(t) == 1
   assert isinstance(t[0], Rest)
   del(t[-1])
   assert len(t) == 0
