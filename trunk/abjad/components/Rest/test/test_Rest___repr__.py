from abjad import *


def test_Rest___repr___01( ):
   '''Rest rest is evaluable.
   '''

   rest = Rest((1, 4))
   new_rest = eval(repr(rest))

   new_rest == rest
