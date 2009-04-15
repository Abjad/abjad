from abjad import *
import py.test


def test_listtools_flatten_01( ):
   l = [1, 2, 3, 4, 5]
   new = listtools.flatten(l)
   assert new == [1, 2, 3, 4, 5]


def test_listtools_flatten_02( ):
   l = [(1, 2), [3, 4]]
   new = listtools.flatten(l)
   assert new == [1, 2, 3, 4]


def test_listtools_flatten_03( ):
   l = [(1, 2), [3, (4, 5)]]
   new = listtools.flatten(l)
   assert new == [1, 2, 3, 4, 5]


def test_listtools_flatten_04( ):
   l = [(1, 2), [3, (4, 5)]]
   new = listtools.flatten(l, ltypes = (list, ))
   assert new == [(1, 2), 3, (4, 5)]


def test_listtools_flatten_05( ):
   l = [(1, 2), [3, (4, 5)]]
   assert py.test.raises(AssertionError, 
      'listtools.flatten(l, ltypes = (tuple, ))')
