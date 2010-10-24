from abjad import *
import py.test


def test_listtools_flatten_iterable_01( ):
   l = [1, 2, 3, 4, 5]
   new = listtools.flatten_iterable(l)
   assert new == [1, 2, 3, 4, 5]


def test_listtools_flatten_iterable_02( ):
   l = [(1, 2), [3, 4]]
   new = listtools.flatten_iterable(l)
   assert new == [1, 2, 3, 4]


def test_listtools_flatten_iterable_03( ):
   l = [(1, 2), [3, (4, 5)]]
   new = listtools.flatten_iterable(l)
   assert new == [1, 2, 3, 4, 5]


def test_listtools_flatten_iterable_04( ):
   l = [(1, 2), [3, (4, 5)]]
   new = listtools.flatten_iterable(l, ltypes = (list, ))
   assert new == [(1, 2), 3, (4, 5)]


def test_listtools_flatten_iterable_05( ):
   l = [(1, 2), [3, (4, 5)]]
   assert py.test.raises(AssertionError, 
      'listtools.flatten_iterable(l, ltypes = (tuple, ))')


def test_listtools_flatten_iterable_06( ):
   l = [1, [2, 3, [4]], 5, [6, 7, [8]]]
   assert listtools.flatten_iterable(l, depth = 0) == [1, [2, 3, [4]], 5, [6, 7, [8]]]
   assert listtools.flatten_iterable(l, depth = 1) == [1, 2, 3, [4], 5, 6, 7, [8]]
   assert listtools.flatten_iterable(l, depth = 2) == [1, 2, 3, 4, 5, 6, 7, 8]
   assert listtools.flatten_iterable(l, depth = 2) == listtools.flatten_iterable(l, depth = 99)
