from abjad import *


def test_durtools_is_duration_pair_01( ):

   assert durtools.is_duration_pair((1, 4))
   assert not durtools.is_duration_pair((1, 2, 3, 4))
   assert not durtools.is_duration_pair(Rational(1, 4))
   assert not durtools.is_duration_pair([(1, 4)])
   assert not durtools.is_duration_pair([Rational(1, 4)])
