from abjad import *


def test_listtools_is_uniform_01( ):

   assert listtools.is_uniform([-1, -1, -1, -1, -1])
   assert listtools.is_uniform([0, 0, 0, 0, 0])
   assert listtools.is_uniform([1, 1, 1, 1, 1])
   assert listtools.is_uniform([2, 2, 2, 2, 2])


def test_listtools_is_uniform_02( ):

   assert not listtools.is_uniform([-1, -1, -1, -1, 99])
   assert not listtools.is_uniform([0, 0, 0, 0, 99])
   assert not listtools.is_uniform([1, 1, 1, 1, 99])
   assert not listtools.is_uniform([2, 2, 2, 2, 99])


def test_listtools_is_uniform_03( ):
   '''Empty iterable boundary case.'''

   assert listtools.is_uniform([ ])
