from abjad import *


def test_Chord_cast_01( ):
   '''Cast noncontainerized chord as note.'''
   c = Chord([2, 3, 4], (1, 4))
   duration = c.duration.written
   n = Note(c)
   assert isinstance(n, Note)
   # check that attributes have not been removed or added.
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert dir(n) == dir(Note(0, (1, 4)))
   assert n.parentage.parent is None
   assert n.duration.written == duration


def test_Chord_cast_02( ):
   '''Cast tupletized chord as note.'''
   t = tuplettools.FixedDurationTuplet((2, 8), Chord([2, 3, 4], (1, 4)) * 3)
   d = t[0].duration.written
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_Chord_cast_03( ):
   '''Cast voice-contained chord as note.'''
   v = Voice(Chord([2, 3, 4], (1, 4)) * 3)
   d = v[0].duration.written
   Note(v[0])
   assert isinstance(v[0], Note)
   assert v[0].parentage.parent is v
   assert v[0].duration.written == d


def test_Chord_cast_04( ):
   '''Cast staff-contained chord as note.'''
   t = Staff(Chord([2, 3, 4], (1, 4)) * 3)
   d = t[0].duration.written
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_Chord_cast_05( ):
   '''Cast beamed chord as note.'''
   t = Staff(Chord([2, 3, 4], (1, 4)) * 3)
   spannertools.BeamSpanner(t[ : ])
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0].parentage.parent is t


def test_Chord_cast_06( ):
   '''Cast noncontainerized chord as rest.'''
   c = Chord([2, 3, 4], (1, 4))
   duration = c.duration.written
   r = Rest(c)
   assert isinstance(r, Rest)
   # check that attributes have not been removed or added.
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert dir(r) == dir(Rest((1, 4)))
   assert r.parentage.parent is None
   assert r.duration.written == duration


def test_Chord_cast_07( ):
   '''Cast tupletized chord as rest.'''
   t = tuplettools.FixedDurationTuplet((2, 8), Chord([2, 3, 4], (1, 4)) * 3)
   d = t[0].duration.written
   Rest(t[0])
   assert isinstance(t[0], Rest)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_Chord_cast_08( ):
   '''Cast voice-contained chord as rest.'''
   v = Voice(Chord([2, 3, 4], (1, 4)) * 3)
   d = v[0].duration.written
   Rest(v[0])
   assert isinstance(v[0], Rest)
   assert v[0].parentage.parent is v
   assert v[0].duration.written == d


def test_Chord_cast_09( ):
   '''Cast staff-contained chord as rest.'''
   t = Staff(Chord([2, 3, 4], (1, 4)) * 3)
   d = t[0].duration.written
   Rest(t[0])
   assert isinstance(t[0], Rest)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_Chord_cast_10( ):
   '''Cast beamed chord as rest.'''
   t = Staff(Chord([2, 3, 4], (1, 4)) * 3)
   spannertools.BeamSpanner(t[ : ])
   Rest(t[0])
   assert isinstance(t[0], Rest)
   assert t[0].parentage.parent is t


def test_Chord_cast_11( ):
   '''Cast noncontainerized chord as skip.'''
   c = Chord([2, 3, 4], (1, 4))
   duration = c.duration.written
   s = Skip(c)
   assert isinstance(s, Skip)
   # check that attributes have not been removed or added.
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert dir(s) == dir(Skip((1, 4)))
   assert s.parentage.parent is None
   assert s.duration.written == duration


def test_Chord_cast_12( ):
   '''Cast tupletized chord as skip.'''
   t = tuplettools.FixedDurationTuplet((2, 8), Chord([2, 3, 4], (1, 4)) * 3)
   d = t[0].duration.written
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_Chord_cast_13( ):
   '''Cast voice-contained chord as skip.'''
   v = Voice(Chord([2, 3, 4], (1, 4)) * 3)
   d = v[0].duration.written
   Skip(v[0])
   assert isinstance(v[0], Skip)
   assert v[0].parentage.parent is v
   assert v[0].duration.written == d


def test_Chord_cast_14( ):
   '''Cast staff-contained chord as skip.'''
   t = Staff(Chord([2, 3, 4], (1, 4)) * 3)
   d = t[0].duration.written
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_Chord_cast_15( ):
   '''Cast beamed chord as skip.'''
   t = Staff(Chord([2, 3, 4], (1, 4)) * 3)
   spannertools.BeamSpanner(t[ : ])
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0].parentage.parent is t
