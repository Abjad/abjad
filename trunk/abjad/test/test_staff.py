from abjad import *
from py.test import raises


### TEST STAFF GETITEM ###

def test_staff_getitem_01( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t, ret = True)
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
   assert check(t, ret = True)
   slice = t[0 : 0]
   assert len(slice) == 0
   assert check(t, ret = True)

def test_staff_getitem_03( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t, ret = True)
   slice = t[0 : 1]
   assert len(slice) == 1
   assert isinstance(slice[0], Note)
   for x in t:
      assert x._parent == t
   assert check(t, ret = True)

def test_staff_getitem_04( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t, ret = True)
   slice = t[-1 : ]
   assert len(slice) == 1
   assert isinstance(slice[0], FixedDurationTuplet)
   for x in slice:
      assert x._parent == t
   assert check(t, ret = True)

def test_staff_getitem_05( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t, ret = True)
   slice = t[1 : -1]
   assert len(slice) == 3
   assert isinstance(slice[0], Rest)
   assert isinstance(slice[1], Chord)
   assert isinstance(slice[2], Skip)
   for x in slice:
      assert x._parent == t
   assert check(t, ret = True)

def test_staff_getitem_06( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t, ret = True)
   slice = t[2 : ]
   assert len(slice) == 3
   assert isinstance(slice[0], Chord)
   assert isinstance(slice[1], Skip)
   assert isinstance(slice[2], FixedDurationTuplet)
   for x in slice:
      assert x._parent == t
   assert check(t, ret = True)

def test_staff_getitem_07( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t, ret = True)
   slice = t[ : -2]
   assert len(slice) == 3
   assert isinstance(slice[0], Note)
   assert isinstance(slice[1], Rest)
   assert isinstance(slice[2], Chord)
   for x in slice:
      assert x._parent == t
   assert check(t, ret = True)

def test_staff_getitem_08( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t, ret = True)
   slice = t[ : ]
   assert len(slice) == 5
   assert isinstance(slice, list)
   assert isinstance(slice[0], Note)
   assert isinstance(slice[1], Rest)
   assert isinstance(slice[2], Chord)
   assert isinstance(slice[3], Skip)
   assert isinstance(slice[4], FixedDurationTuplet)
   for x in slice:
      assert x._parent == t
   assert check(t, ret = True)


### TEST STAFF SETITEM ###

def test_staff_setitem_01( ):
   t = Staff([Note(0, (1, 4)),
         Rest((1, 4)),
         Chord([2, 3, 4], (1, 4)),
         Skip((1, 4)),
         FixedDurationTuplet((5, 16), Note(0, (1, 16)) * 4)])
   assert len(t) == 5
   assert check(t, ret = True)
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Rest)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], Skip)
   assert isinstance(t[4], FixedDurationTuplet)
   t[1] = Chord([12, 13, 15], (1, 4))
   assert len(t) == 5
   assert check(t, ret = True)
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], Skip)
   assert isinstance(t[4], FixedDurationTuplet)
   t[0] = Rest((1, 4))
   assert len(t) == 5
   assert check(t, ret = True)
   assert isinstance(t[0], Rest)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], Skip)
   assert isinstance(t[4], FixedDurationTuplet)
   t[-2] = FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   assert len(t) == 5
   assert check(t, ret = True)
   assert isinstance(t[0], Rest)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], FixedDurationTuplet)
   assert isinstance(t[4], FixedDurationTuplet)
   t[-1] = Note(13, (1, 4))
   assert len(t) == 5
   assert check(t, ret = True)
   assert isinstance(t[0], Rest)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Chord)
   assert isinstance(t[3], FixedDurationTuplet)
   assert isinstance(t[4], Note)
   t[-3] = Skip((1, 4))
   assert len(t) == 5
   assert check(t, ret = True)
   assert isinstance(t[0], Rest)
   assert isinstance(t[1], Chord)
   assert isinstance(t[2], Skip)
   assert isinstance(t[3], FixedDurationTuplet)
   assert isinstance(t[4], Note)

def test_staff_setitem_02( ):
   '''Reassign the *entire* contents of t.'''
   t = Staff(Note(0, (1, 4)) * 4)
   assert t.duration == Rational(4, 4)
   t[ : ] = Note(0, (1, 8)) * 4
   assert t.duration == Rational(4, 8)

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
   assert raises(AssertionError, 't[0] = [Note(2, (1, 4)), Note(2, (1, 4))]')

def test_staff_setitem_06( ):
   '''Bark when user assigns an item to a slice.'''
   t = Staff(Note(0, (1, 4)) * 4)
   assert raises(AssertionError, 't[0 : 2] = Note(2, (1, 4))')

def test_staff_setitem_07( ):
   '''Slice-assign notes.'''
   t = Staff(Note(0, (1, 8)) * 8)
   t[0 : 4] = Note(2, (1, 8)) * 4
   assert len(t) == 8
   for x in t[0 : 4]:
      assert x.pitch == Pitch(2)
   for x in t[4 : 8]:
      assert x.pitch == Pitch(0)
   assert check(t, ret = True)

def test_staff_setitem_08( ):
   '''Slice-assign chords.'''
   t = Staff(Note(0, (1, 8)) * 8)
   t[0 : 4] = Chord([2, 3, 4], (1, 4)) * 4
   assert len(t) == 8
   for x in t[0 : 4]:
      assert x.duration == Rational(1, 4)
   for x in t[4 : 8]:
      assert x.duration == Rational(1, 8)
   assert check(t, ret = True)

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
   assert check(t, ret = True)

def test_staff_setitem_10( ):
   '''Slice-assign measures.'''
   t = Staff(Note(0, (1, 8)) * 8)
   t[0 : 4] = Measure((2, 8), Note(0, (1, 8)) * 2) * 2
   assert len(t) == 6
   for i, x in enumerate(t):
      if i in [0, 1]:
         assert isinstance(x, Measure)
      else:
         assert isinstance(x, Note)
   assert check(t, ret = True)



### TEST STAFF DEL ###

def test_staff_del_01( ):
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

def test_staff_del_02( ):
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

def test_del_staff_03( ):
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


### TEST STAFF APPEND ###

def test_staff_append_01( ):
   t = Staff(Note(0, (1, 4)) * 4)
   t.append(Note(0, (1, 4)))
   assert check(t, ret = True)
   assert len(t) == 5
   assert t.duration == Rational(5, 4)

def test_staff_append_02( ):
   t = Staff(Note(0, (1, 4)) * 4)
   t.append(Chord([2, 3, 4], (1, 4)))
   assert check(t, ret = True)
   assert len(t) == 5
   assert t.duration == Rational(5, 4)

def test_staff_append_03( ):
   t = Staff(Note(0, (1, 4)) * 4)
   t.append(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3))
   assert check(t, ret = True)
   assert len(t) == 5
   assert t.duration == Rational(5, 4)

def test_staff_append_04( ):
   '''Empty containers are allowed but not well-formed.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t.append(FixedDurationTuplet((2, 8), [ ]))
   assert len(t) == 5
   assert t.duration == Rational(5, 4)


### TEST SET STAFF INVOCATION ###

def test_set_staff_invocation_01( ):
   t = Staff([ ])
   t.invocation.lhs = 'RhythmicStaff'
   assert repr(t.invocation) == '_Invocation(RhythmicStaff)'
   assert t.format == '\\new RhythmicStaff {\n}'
