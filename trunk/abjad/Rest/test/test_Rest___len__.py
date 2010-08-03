from abjad import *


def test_Rest___len___01( ):

   t = Rest((1, 4))
   assert len(t) == 0
