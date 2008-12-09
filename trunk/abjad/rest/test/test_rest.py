from abjad import *


def test_rest_01( ):
   '''Typical rest.'''
   r = Rest((1, 4))
   assert repr(r) == 'Rest(4)'
   assert r.format == 'r4'
   assert r.duration.written == r.duration.prolated == Rational(1, 4)
