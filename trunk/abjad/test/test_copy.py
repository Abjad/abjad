from abjad import *


### TEST COPY ONE LEAF ###

def test_copy_note_01( ):
   m = Note(0, (1, 8))
   n = m.copy( )
   assert id(m) != id(n)
   assert m._parent is None
   assert n._parent is None

def test_copy_rest_01( ):
   r = Rest((1, 8))
   s = r.copy( )
   assert id(r) != id(s)
   assert r._parent is None
   assert s._parent is None

def test_copy_skip_01( ):
   s = Skip((1, 8))
   t = s.copy( )
   assert id(s) != id(t)
   assert s._parent is None
   assert t._parent is None

def test_copy_chord_01( ):
   d = Chord([2, 3, 4], (1, 4))
   e = d.copy( )
   assert id(d) != id(e)
   assert d._parent is None
   assert e._parent is None

def test_tuplet_copy_note_01( ):
   t = FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)
   m = t[1]
   n = m.copy( )
   assert id(m) != id(n)
   assert m._parent is t
   assert n._parent is None


### TEST COPY ONE CONTAINER ###

def test_copy_complete_container_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   u = t.copy( )
   id(u) is not id(t)
   check(t)
   check(u)


### TEST COPY ONE TUPLETIZED NOTE ###

def test_copy_one_tupletized_note_01( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = t.leaves[4].copy( )
   assert isinstance(u, Note)
   assert u.pitch == t.leaves[4].pitch
   assert u.duration == t.leaves[4].duration
   assert id(u) != id(t.leaves[4])
   assert u.duration.prolated != t.leaves[4].duration.prolated

def test_copy_one_tupletized_note_02( ):
   t = Staff(FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3) * 3)
   u = t.leaves[5].copy( )
   assert isinstance(u, Note)
   assert u.pitch == t.leaves[5].pitch
   assert u.duration == t.leaves[5].duration
   assert id(u) != id(t.leaves[5])
   assert u.duration.prolated != t.leaves[5].duration.prolated
