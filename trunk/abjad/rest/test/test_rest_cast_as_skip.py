from abjad import *


def test_rest_cast_as_skip_01( ):
   r = Rest((1, 8))
   d = r.duration.written
   s = Skip(r)
   assert isinstance(s, Skip)
   # check that attributes have not been removed or added.
   assert dir(r) == dir(Rest((1, 4)))
   assert dir(s) == dir(Skip((1, 4)))
   assert s.parentage.parent is None
   assert s.duration.written == d


def test_rest_cast_as_skip_02( ):
   t = FixedDurationTuplet((2, 8), Rest((1, 8)) * 3)
   d = t[0].duration.written
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_rest_cast_as_skip_03( ):
   v = Voice(Rest((1, 8)) * 3)
   d = v[0].duration.written
   Skip(v[0])
   assert isinstance(v[0], Skip)
   assert v[0].parentage.parent is v
   assert v[0].duration.written == d


def test_rest_cast_as_skip_04( ):
   t = Staff(Rest((1, 8)) * 3)
   d = t[0].duration.written
   Skip(t[0])
   assert isinstance(t[0], Skip)
   assert t[0].parentage.parent is t
   assert t[0].duration.written == d


def test_rest_cast_as_skip_05( ):
   '''Works fine when rest is beamed.'''
   t = Staff([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
   Beam(t[ : ])
   Skip(t[1])
   assert isinstance(t[1], Skip)
   assert t[1].parentage.parent is t
