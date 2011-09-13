from abjad import *


# TODO: remove test file #
#def test_TieSpanner_01():
#
#   t = Voice("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
#   p = tietools.TieSpanner(t[4:6])
#
#   assert len(p) == 2
#
#   assert not t[0].tie.spanned
#   assert not t[1].tie.spanned
#   assert not t[2].tie.spanned
#   assert not t[3].tie.spanned
#   assert t[4].tie.spanned
#   assert t[5].tie.spanned
#   assert not t[6].tie.spanned
#   assert not t[7].tie.spanned
#
#   assert t[4].tie.spanner is t[5].tie.spanner
