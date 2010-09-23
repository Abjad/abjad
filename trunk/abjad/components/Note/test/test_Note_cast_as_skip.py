from abjad import *
from py.test import raises
import py
py.test.skip('make casting work before deprecating casting.')


def test_Note_cast_as_skip_01( ):
   n = Note(2, (1, 8))
   d = n.duration.written
   s = Skip(n)
   assert isinstance(s, Skip)
   # check that attributes have not been removed or added.
   assert dir(n) == dir(Note(0, (1, 4)))
   assert dir(s) == dir(Skip((1, 4)))
   assert s.format == 's8'
   assert s._parentage.parent is None
   assert s.duration.written == d


def test_Note_cast_as_skip_02( ):
   t = tuplettools.FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   d = t[0].duration.written
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0].format == 's8'
   assert t[0]._parentage.parent is t
   assert t[0].duration.written == d


def test_Note_cast_as_skip_03( ):
   v = Voice(Note(0, (1, 8)) * 3)
   d = v[0].duration.written
   Skip(v[0])
   assert isinstance(v[0], Skip)
   assert v[0].format == 's8'
   assert v[0]._parentage.parent is v
   assert v[0].duration.written == d


def test_Note_cast_as_skip_04( ):
   t = Staff(Note(0, (1, 8)) * 3)
   d = t[0].duration.written
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0].format == 's8'
   assert t[0]._parentage.parent is t
   assert t[0].duration.written == d


def test_Note_cast_as_skip_05( ):
   '''Works fine when note is beamed.'''
   t = Staff(Note(0, (1, 8)) * 3)
   spannertools.BeamSpanner(t[:])
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0]._parentage.parent is t
