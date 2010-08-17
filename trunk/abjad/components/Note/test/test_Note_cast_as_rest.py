from abjad import *
from py.test import raises
import py
py.test.skip('make casting work again before deprecating casting.')


def test_Note_cast_as_rest_01( ):
   n = Note(2, (1, 8))
   d = n.duration.written
   r = Rest(n)
   assert isinstance(r, Rest)
   # check that attributes have not been removed or added.
   assert dir(n) == dir(Note(0, (1, 8)))
   assert dir(r) == dir(Rest((1, 4)))
   assert r.format == 'r8'
   assert r.parentage.parent is None
   assert r.duration.written == d


def test_Note_cast_as_rest_02( ):
   t = FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   d = t[0].duration.written
   Rest(t[0])
   assert t[0].format == 'r8'
   assert isinstance(t[0], Rest)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_Note_cast_as_rest_03( ):
   v = Voice(Note(0, (1, 8)) * 3)
   d = v[0].duration.written
   Rest(v[0])
   assert v[0].format == 'r8'
   assert isinstance(v[0], Rest)
   assert v[0].parentage.parent is v
   assert v[0].duration.written == d


def test_Note_cast_as_rest_04( ):
   t = Staff(Note(0, (1, 8)) * 3)
   d = t[0].duration.written
   Rest(t[0])
   assert t[0].format == 'r8'
   assert isinstance(t[0], Rest)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_Note_cast_as_rest_05( ):
   '''Works fine when note is beamed.'''
   t = Staff(Note(0, (1, 8)) * 3)
   spannertools.BeamSpanner(t[ : ])
   Rest(t[0])
   assert isinstance(t[0], Rest)
   assert t[0].parentage.parent is t


def test_Note_cast_as_rest_06( ):
   '''Spanner interface references emerge correctly from casting.'''
   t = Note(0, (1, 4))
   r = Rest(t)
   assert t.spanners._client is t
   assert r.spanners._client is r
