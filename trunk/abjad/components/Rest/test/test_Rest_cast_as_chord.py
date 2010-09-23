from abjad import *


def test_Rest_cast_as_chord_01( ):
   r = Rest((1, 8))
   d = r.duration.written
   c = Chord(r)
   assert isinstance(c, Chord)
   # check that attributes have not been removed or added.
   assert dir(r) == dir(Rest((1, 4)))
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert c._parentage.parent is None
   assert c.duration.written == d


def test_Rest_cast_as_chord_02( ):
   t = tuplettools.FixedDurationTuplet((2, 8), Rest((1, 8)) * 3)
   d = t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0]._parentage.parent is t
   assert t[0].duration.written == d


def test_Rest_cast_as_chord_03( ):
   v = Voice(Rest((1, 8)) * 3)
   d = v[0].duration.written
   Chord(v[0])
   assert isinstance(v[0], Chord)
   assert v[0]._parentage.parent is v
   assert v[0].duration.written == d


def test_Rest_cast_as_chord_04( ):
   t = Staff(Rest((1, 8)) * 3)
   d = t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0]._parentage.parent is t
   assert t[0].duration.written == d


def test_Rest_cast_as_chord_05( ):
   '''Works fine when rest is beamed.'''
   t = Staff([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
   spannertools.BeamSpanner(t[:])
   Chord(t[1])
   assert isinstance(t[1], Chord)
   assert t[1]._parentage.parent is t
