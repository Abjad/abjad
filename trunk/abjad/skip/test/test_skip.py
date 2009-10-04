from abjad import *


### TEST DEMO SKIP PUBLIC INTERFACE ###

def test_skip_01( ):
   s = Skip((1, 8))
   assert repr(s) == 'Skip(8)'
   assert str(s) == 's8'
   assert s.format == 's8'
   assert s.duration.written == s.duration.prolated == Rational(1, 8)


def test_skip_02( ):
   s = Skip((3, 16))
   assert repr(s) == 'Skip(8.)'
   assert str(s) == 's8.'
   assert s.format == 's8.'
   assert s.duration.written == s.duration.prolated == Rational(3, 16)


### TEST CAST SKIP AS NOTE ###

def test_skip_03( ):
   s = Skip((1, 8))
   d = s.duration.written
   n = Note(s)
   assert isinstance(n, Note)
   # check that attributes have not been removed or added.
   assert dir(s) == dir(Skip((1, 4)))
   assert dir(n) == dir(Note(0, (1, 4)))
   assert n.parentage.parent is None
   assert n.duration.written == d


def test_skip_04( ):
   t = FixedDurationTuplet((2, 8), Skip((1, 8)) * 3)
   d = t[0].duration.written
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_skip_05( ):
   v = Voice(Skip((1, 8)) * 3)
   d = v[0].duration.written
   Note(v[0])
   assert isinstance(v[0], Note)
   assert v[0].parentage.parent is v
   assert v[0].duration.written == d


def test_skip_06( ):
   t = Staff(Skip((1, 8)) * 3)
   d = t[0].duration.written
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_skip_07( ):
   '''Works fine when skip is beamed.'''
   t = Staff([Note(0, (1, 8)), Skip((1, 8)), Note(0, (1, 8))])
   Beam(t[ : ])
   Note(t[1])
   assert isinstance(t[1], Note)
   assert t[1].parentage.parent is t
   


### TEST CAST SKIP AS REST ###

def test_skip_08( ):
   s = Skip((1, 8))
   d = s.duration.written
   r = Rest(s)
   assert isinstance(r, Rest)
   # check that attributes have not been removed or added.
   assert dir(s) == dir(Skip((1, 4)))
   assert dir(r) == dir(Rest((1, 4)))
   assert r.parentage.parent is None
   assert r.duration.written == d


def test_skip_09( ):
   t = FixedDurationTuplet((2, 8), Skip((1, 8)) * 3)
   d = t[0].duration.written
   Rest(t[0])
   assert isinstance(t[0], Rest)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_skip_10( ):
   v = Voice(Skip((1, 8)) * 3)
   d = v[0].duration.written
   Rest(v[0])
   assert isinstance(v[0], Rest)
   assert v[0].parentage.parent is v
   assert v[0].duration.written == d


def test_skip_11( ):
   t = Staff(Skip((1, 8)) * 3)
   d = t[0].duration.written
   Rest(t[0])
   assert isinstance(t[0], Rest)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_skip_12( ):
   '''Works fine when skip is beamed.'''
   t = Staff([Note(0, (1, 8)), Skip((1, 8)), Note(0, (1, 8))])
   Beam(t[ : ])
   Rest(t[1])
   assert isinstance(t[1], Rest)
   assert t[1].parentage.parent is t


### TEST CAST REST AS CHORD ###

def test_skip_13( ):
   s = Skip((1, 8))
   d = s.duration.written
   c = Chord(s)
   assert isinstance(c, Chord)
   # check that attributes have not been removed or added.
   assert dir(s) == dir(Skip((1, 4)))
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert c.parentage.parent is None
   assert c.duration.written == d


def test_skip_14( ):
   t = FixedDurationTuplet((2, 8), Skip((1, 8)) * 3)
   d = t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_skip_15( ):
   v = Voice(Skip((1, 8)) * 3)
   d = v[0].duration.written
   Chord(v[0])
   assert isinstance(v[0], Chord)
   assert v[0].parentage.parent is v
   assert v[0].duration.written == d


def test_skip_16( ):
   t = Staff(Skip((1, 8)) * 3)
   d = t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_skip_17( ):
   '''Works fine when skip is beamed.'''
   t = Staff([Note(0, (1, 8)), Skip((1, 8)), Note(0, (1, 8))])
   Beam(t[ : ])
   Chord(t[1])
   assert isinstance(t[1], Chord)
   assert t[1].parentage.parent is t
