from abjad import *


def test_listtools_get_shared_numeric_sign_01( ):

   assert listtools.get_shared_numeric_sign([1, 2, 3]) == 1
   assert listtools.get_shared_numeric_sign([-1, -2, -3]) == -1
   assert listtools.get_shared_numeric_sign([ ]) == 0
   assert listtools.get_shared_numeric_sign([1, 2, -3]) is None
