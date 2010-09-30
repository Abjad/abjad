from abjad import *


def test_Skip_01( ):
   '''skiptools.Skip public interface.'''
   s = skiptools.Skip((1, 8))
   assert repr(s) == 'Skip(8)'
   assert str(s) == 's8'
   assert s.format == 's8'
   assert s.duration.written == s.duration.prolated == Fraction(1, 8)


def test_Skip_02( ):
   s = skiptools.Skip((3, 16))
   assert repr(s) == 'Skip(8.)'
   assert str(s) == 's8.'
   assert s.format == 's8.'
   assert s.duration.written == s.duration.prolated == Fraction(3, 16)


def test_Skip_03( ):
   '''Cast skip as note.'''
   s = skiptools.Skip((1, 8))
   d = s.duration.written
   n = Note(s)
   assert isinstance(n, Note)
   assert dir(s) == dir(skiptools.Skip((1, 4)))
   assert dir(n) == dir(Note(0, (1, 4)))
   assert n._parentage.parent is None
   assert n.duration.written == d


def test_Skip_04( ):
   t = tuplettools.FixedDurationTuplet((2, 8), skiptools.Skip((1, 8)) * 3)
   d = t[0].duration.written
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0]._parentage.parent is t
   assert t[0].duration.written == d


def test_Skip_05( ):
   v = Voice(skiptools.Skip((1, 8)) * 3)
   d = v[0].duration.written
   Note(v[0])
   assert isinstance(v[0], Note)
   assert v[0]._parentage.parent is v
   assert v[0].duration.written == d


def test_Skip_06( ):
   t = Staff(skiptools.Skip((1, 8)) * 3)
   d = t[0].duration.written
   Note(t[0])
   assert isinstance(t[0], Note)
   assert t[0]._parentage.parent is t
   assert t[0].duration.written == d


def test_Skip_07( ):
   '''Works fine when skip is beamed.'''
   t = Staff([Note(0, (1, 8)), skiptools.Skip((1, 8)), Note(0, (1, 8))])
   spannertools.BeamSpanner(t[:])
   Note(t[1])
   assert isinstance(t[1], Note)
   assert t[1]._parentage.parent is t
   

def test_Skip_08( ):
   '''Cast skip as rest.'''
   s = skiptools.Skip((1, 8))
   d = s.duration.written
   r = Rest(s)
   assert isinstance(r, Rest)
   assert dir(s) == dir(skiptools.Skip((1, 4)))
   assert dir(r) == dir(Rest((1, 4)))
   assert r._parentage.parent is None
   assert r.duration.written == d


def test_Skip_09( ):
   t = tuplettools.FixedDurationTuplet((2, 8), skiptools.Skip((1, 8)) * 3)
   d = t[0].duration.written
   Rest(t[0])
   assert isinstance(t[0], Rest)
   assert t[0]._parentage.parent is t
   assert t[0].duration.written == d


def test_Skip_10( ):
   v = Voice(skiptools.Skip((1, 8)) * 3)
   d = v[0].duration.written
   Rest(v[0])
   assert isinstance(v[0], Rest)
   assert v[0]._parentage.parent is v
   assert v[0].duration.written == d


def test_Skip_11( ):
   t = Staff(skiptools.Skip((1, 8)) * 3)
   d = t[0].duration.written
   Rest(t[0])
   assert isinstance(t[0], Rest)
   assert t[0]._parentage.parent is t
   assert t[0].duration.written == d


def test_Skip_12( ):
   '''Works fine when skip is beamed.'''
   t = Staff([Note(0, (1, 8)), skiptools.Skip((1, 8)), Note(0, (1, 8))])
   spannertools.BeamSpanner(t[:])
   Rest(t[1])
   assert isinstance(t[1], Rest)
   assert t[1]._parentage.parent is t


def test_Skip_13( ):
   '''Cast skip as chord.'''
   s = skiptools.Skip((1, 8))
   d = s.duration.written
   c = Chord(s)
   assert isinstance(c, Chord)
   assert dir(s) == dir(skiptools.Skip((1, 4)))
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert c._parentage.parent is None
   assert c.duration.written == d


def test_Skip_14( ):
   t = tuplettools.FixedDurationTuplet((2, 8), skiptools.Skip((1, 8)) * 3)
   d = t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0]._parentage.parent is t
   assert t[0].duration.written == d


def test_Skip_15( ):
   v = Voice(skiptools.Skip((1, 8)) * 3)
   d = v[0].duration.written
   Chord(v[0])
   assert isinstance(v[0], Chord)
   assert v[0]._parentage.parent is v
   assert v[0].duration.written == d


def test_Skip_16( ):
   t = Staff(skiptools.Skip((1, 8)) * 3)
   d = t[0].duration.written
   Chord(t[0])
   assert isinstance(t[0], Chord)
   assert t[0]._parentage.parent is t
   assert t[0].duration.written == d


def test_Skip_17( ):
   '''Works fine when skip is beamed.'''
   t = Staff([Note(0, (1, 8)), skiptools.Skip((1, 8)), Note(0, (1, 8))])
   spannertools.BeamSpanner(t[:])
   Chord(t[1])
   assert isinstance(t[1], Chord)
   assert t[1]._parentage.parent is t
