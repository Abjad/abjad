from abjad import *


def test_listtools_is_restricted_growth_function_01( ):

   assert listtools.is_restricted_growth_function([1, 1, 1, 1])
   assert listtools.is_restricted_growth_function([1, 1, 1, 2])
   assert listtools.is_restricted_growth_function([1, 1, 2, 1])
   assert listtools.is_restricted_growth_function([1, 1, 2, 2])
   assert listtools.is_restricted_growth_function([1, 1, 2, 3])
   assert listtools.is_restricted_growth_function([1, 2, 1, 1])
   assert listtools.is_restricted_growth_function([1, 2, 1, 2])
   assert listtools.is_restricted_growth_function([1, 2, 1, 3])
   assert listtools.is_restricted_growth_function([1, 2, 2, 1])
   assert listtools.is_restricted_growth_function([1, 2, 2, 2])
   assert listtools.is_restricted_growth_function([1, 2, 2, 3])
   assert listtools.is_restricted_growth_function([1, 2, 3, 1])
   assert listtools.is_restricted_growth_function([1, 2, 3, 2])
   assert listtools.is_restricted_growth_function([1, 2, 3, 3])
   assert listtools.is_restricted_growth_function([1, 2, 3, 4])


def test_listtools_is_restricted_growth_function_02( ):

   assert not listtools.is_restricted_growth_function([1, 1, 1, 3])
   assert not listtools.is_restricted_growth_function([1, 1, 3, 3])
   assert not listtools.is_restricted_growth_function([1, 3, 1, 3])
   assert not listtools.is_restricted_growth_function([3, 1, 1, 3])
