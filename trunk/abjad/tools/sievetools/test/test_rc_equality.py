from abjad.tools.sievetools.rc import RC
from abjad.tools.sievetools.rcexpression import RCexpression
import py.test


def test_rc_equality_01( ):
   '''non-equal residue classes'''

   t1 = RC(2, 1)
   t2 = RC(3, 1)

   assert t1 != t2


def test_rc_equality_02( ):
   '''non-equal objects'''

   t = RC(2, 1)

   assert t != 'a'
   assert 2 != t


def test_rc_equality_03( ):
   '''equal'''

   t1 = RC(2, 1)
   t2 = RC(2, 1)

   assert t1 == t2
