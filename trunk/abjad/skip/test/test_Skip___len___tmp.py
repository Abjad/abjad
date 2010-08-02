from abjad import *


def test_skip___len___01( ):

   t = Skip((1, 4))
   assert len(t) == 0
