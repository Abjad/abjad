from abjad import *


def test_cast_note_01( ):
   r = Rest((1, 8))
   d = r.duration.written
   n = Note(r)
   assert isinstance(n, Note)
   # check that attributes have not been removed or added.
   assert dir(r) == dir(Rest((1, 4)))
   assert dir(n) == dir(Note(0, (1, 4)))
   assert n._parent is None
   assert n.duration.written == d


def test_cast_note_02( ):
   t = FixedDurationTuplet((2, 8), Rest((1, 8)) * 3)
   d = t[0].duration.written
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0]._parent is t
   assert t[0].duration.written == d


def test_cast_note_03( ):
   v = Voice(Rest((1, 8)) * 3)
   d = v[0].duration.written
   Note(v[0])
   assert isinstance(v[0], Note)
   assert v[0]._parent is v
   assert v[0].duration.written == d


def test_cast_note_04( ):
   t = Staff(Rest((1, 8)) * 3)
   d = t[0].duration.written
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0]._parent is t
   assert t[0].duration.written == d


def test_cast_note_05( ):
   '''Works fine when rest is beamed.'''
   t = Staff([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
   #Beam(t)
   Beam(t[ : ])
   Note(t[1])
   assert isinstance(t[1], Note)
   assert t[1]._parent is t
