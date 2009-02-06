from abjad.helpers.is_duration_pair import _is_duration_pair
from abjad.rational.rational import Rational

def test_is_duration_pair_01( ):
   assert _is_duration_pair((1, 4))
   assert not _is_duration_pair((1, 2, 3, 4))
   assert not _is_duration_pair(Rational(1, 4))
   assert not _is_duration_pair([(1, 4)])
   assert not _is_duration_pair([Rational(1, 4)])
