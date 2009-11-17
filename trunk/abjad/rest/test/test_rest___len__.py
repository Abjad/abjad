from abjad import *


def test_rest___len___01( ):

   t = Rest((1, 4))
   assert len(t) == 0
