from abjad import *


def test_listtools_sign_01( ):

   assert listtools.sign([1, 2, 3]) == 1
   assert listtools.sign([-1, -2, -3]) == -1
   assert listtools.sign([ ]) == 0
   assert listtools.sign([1, 2, -3]) is None
