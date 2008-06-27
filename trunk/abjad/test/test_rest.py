from abjad import *


### TEST TYPICAL REST ###

def test_typical_rest_01( ):
   r = Rest((1, 4))
   assert repr(r) == 'Rest(4)'
   assert r.format == 'r4'
   assert r.duration.written == r.duration.prolated == Rational(1, 4)


### TEST PITCHED REST ###

def test_pitched_rest_01( ):
   '''Rests can have pitch set with int.'''
   r = Rest((1, 4))
   r.pitch = 0
   assert isinstance(r.pitch, Pitch)
   assert repr(r) == 'Rest(4)'
   assert r.format == "c'4 \\rest"
   assert r.duration.written == r.duration.prolated == Rational(1, 4)


def test_pitched_rest_02( ):
   '''Rests can have pitch set with Pitch.'''
   r = Rest((1, 4))
   r.pitch = Pitch(0)
   assert isinstance(r.pitch, Pitch)
   assert repr(r) == 'Rest(4)'
   assert r.format == "c'4 \\rest"
   assert r.duration.written == r.duration.prolated == Rational(1, 4)


def test_pitched_rest_03( ):
   '''Rests can have pitch set to None.'''
   r = Rest((1, 4))
   r.pitch = None
   assert isinstance(r.pitch, type(None))
   assert repr(r) == 'Rest(4)'
   assert r.format == "r4"
   assert r.duration.written == r.duration.prolated == Rational(1, 4)


### TEST CAST REST AS NOTE ###

def test_cast_rest_as_note_01( ):
   r = Rest((1, 8))
   d = r.duration.written
   n = Note(r)
   assert isinstance(n, Note)
   # check that attributes have not been removed or added.
   assert dir(r) == dir(Rest((1, 4)))
   assert dir(n) == dir(Note(0, (1, 4)))
   assert n._parent is None
   assert n.duration.written == d


def test_cast_rest_as_note_02( ):
   t = FixedDurationTuplet((2, 8), Rest((1, 8)) * 3)
   d = t[0].duration.written
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0]._parent is t
   assert t[0].duration.written == d


def test_cast_rest_as_note_03( ):
   v = Voice(Rest((1, 8)) * 3)
   d = v[0].duration.written
   Note(v[0])
   assert isinstance(v[0], Note)
   assert v[0]._parent is v
   assert v[0].duration.written == d


def test_cast_rest_as_note_04( ):
   t = Staff(Rest((1, 8)) * 3)
   d = t[0].duration.written
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0]._parent is t
   assert t[0].duration.written == d


def test_cast_rest_as_note_05( ):
   '''Works fine when rest is beamed.'''
   t = Staff([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
   Beam(t)
   Note(t[1])
   assert isinstance(t[1], Note)
   assert t[1]._parent is t


### TEST CAST REST AS CHORD ###

def test_cast_rest_as_chord_01( ):
   r = Rest((1, 8))
   d = r.duration.written
   c = Chord(r)
   assert isinstance(c, Chord)
   # check that attributes have not been removed or added.
   assert dir(r) == dir(Rest((1, 4)))
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert c._parent is None
   assert c.duration.written == d


def test_cast_rest_as_chord_02( ):
   t = FixedDurationTuplet((2, 8), Rest((1, 8)) * 3)
   d = t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0]._parent is t
   assert t[0].duration.written == d


def test_cast_rest_as_chord_03( ):
   v = Voice(Rest((1, 8)) * 3)
   d = v[0].duration.written
   Chord(v[0])
   assert isinstance(v[0], Chord)
   assert v[0]._parent is v
   assert v[0].duration.written == d


def test_cast_rest_as_chord_04( ):
   t = Staff(Rest((1, 8)) * 3)
   d = t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0]._parent is t
   assert t[0].duration.written == d


def test_cast_rest_as_chord_05( ):
   '''Works fine when rest is beamed.'''
   t = Staff([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
   Beam(t)
   Chord(t[1])
   assert isinstance(t[1], Chord)
   assert t[1]._parent is t


### TEST CAST REST AS SKIP ###

def test_cast_rest_as_skip_01( ):
   r = Rest((1, 8))
   d = r.duration.written
   s = Skip(r)
   assert isinstance(s, Skip)
   # check that attributes have not been removed or added.
   assert dir(r) == dir(Rest((1, 4)))
   assert dir(s) == dir(Skip((1, 4)))
   assert s._parent is None
   assert s.duration.written == d


def test_cast_rest_as_skip_02( ):
   t = FixedDurationTuplet((2, 8), Rest((1, 8)) * 3)
   d = t[0].duration.written
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0]._parent is t
   assert t[0].duration.written == d


def test_cast_rest_as_skip_03( ):
   v = Voice(Rest((1, 8)) * 3)
   d = v[0].duration.written
   Skip(v[0])
   assert isinstance(v[0], Skip)
   assert v[0]._parent is v
   assert v[0].duration.written == d


def test_cast_rest_as_skip_04( ):
   t = Staff(Rest((1, 8)) * 3)
   d = t[0].duration.written
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0]._parent is t
   assert t[0].duration.written == d


def test_cast_rest_as_skip_05( ):
   '''Works fine when rest is beamed.'''
   t = Staff([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
   Beam(t)
   Skip(t[1])
   assert isinstance(t[1], Skip)
   assert t[1]._parent is t
