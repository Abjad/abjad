from abjad import *


### TEST DEMO SKIP PUBLIC INTERFACE ###

def test_demo_skip_public_interface_01( ):
   s = Skip((1, 8))
   assert repr(s) == 'Skip(8)'
   assert str(s) == 's8'
   assert s.format == 's8'
   assert s.duration.written == s.duration.absolute == Rational(1, 8)


def test_demo_skip_public_interface_02( ):
   s = Skip((3, 16))
   assert repr(s) == 'Skip(8.)'
   assert str(s) == 's8.'
   assert s.format == 's8.'
   assert s.duration.written == s.duration.absolute == Rational(3, 16)


### TEST CAST SKIP AS NOTE ###

def test_cast_skip_as_note_01( ):
   s = Skip((1, 8))
   d = s.duration.written
   n = Note(s)
   assert isinstance(n, Note)
   # check that attributes have not been removed or added.
   assert dir(s) == dir(Skip((1, 4)))
   assert dir(n) == dir(Note(0, (1, 4)))
   assert n._parent is None
   assert n.duration.written == d


def test_cast_skip_as_note_02( ):
   t = FixedDurationTuplet((2, 8), Skip((1, 8)) * 3)
   d = t[0].duration.written
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0]._parent is t
   assert t[0].duration.written == d


def test_cast_skip_as_note_03( ):
   v = Voice(Skip((1, 8)) * 3)
   d = v[0].duration.written
   Note(v[0])
   assert isinstance(v[0], Note)
   assert v[0]._parent is v
   assert v[0].duration.written == d


def test_cast_skip_as_note_04( ):
   t = Staff(Skip((1, 8)) * 3)
   d = t[0].duration.written
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0]._parent is t
   assert t[0].duration.written == d


### TEST CAST SKIP AS REST ###

def test_cast_skip_as_rest_01( ):
   s = Skip((1, 8))
   d = s.duration.written
   r = Rest(s)
   assert isinstance(r, Rest)
   # check that attributes have not been removed or added.
   assert dir(s) == dir(Skip((1, 4)))
   assert dir(r) == dir(Rest((1, 4)))
   assert r._parent is None
   assert r.duration.written == d


def test_cast_skip_as_rest_02( ):
   t = FixedDurationTuplet((2, 8), Skip((1, 8)) * 3)
   d = t[0].duration.written
   Rest(t[0])
   assert isinstance(t[0], Rest)
   assert t[0]._parent is t
   assert t[0].duration.written == d


def test_cast_skip_as_rest_03( ):
   v = Voice(Skip((1, 8)) * 3)
   d = v[0].duration.written
   Rest(v[0])
   assert isinstance(v[0], Rest)
   assert v[0]._parent is v
   assert v[0].duration.written == d


def test_cast_skip_as_rest_04( ):
   t = Staff(Skip((1, 8)) * 3)
   d = t[0].duration.written
   Rest(t[0])
   assert isinstance(t[0], Rest)
   assert t[0]._parent is t
   assert t[0].duration.written == d


### TEST CAST REST AS CHORD ###

def test_cast_skip_as_chord_01( ):
   s = Skip((1, 8))
   d = s.duration.written
   c = Chord(s)
   assert isinstance(c, Chord)
   # check that attributes have not been removed or added.
   assert dir(s) == dir(Skip((1, 4)))
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert c._parent is None
   assert c.duration.written == d


def test_cast_skip_as_chord_02( ):
   t = FixedDurationTuplet((2, 8), Skip((1, 8)) * 3)
   d = t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0]._parent is t
   assert t[0].duration.written == d


def test_cast_skip_as_chord_03( ):
   v = Voice(Skip((1, 8)) * 3)
   d = v[0].duration.written
   Chord(v[0])
   assert isinstance(v[0], Chord)
   assert v[0]._parent is v
   assert v[0].duration.written == d


def test_cast_skip_as_chord_04( ):
   t = Staff(Skip((1, 8)) * 3)
   d = t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0]._parent is t
   assert t[0].duration.written == d
