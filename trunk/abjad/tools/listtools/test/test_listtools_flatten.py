from abjad import *


def test_listtools_flatten_01( ):
   l = [1, 2, 3, 4, 5]
   r = listtools.flatten(l)
   assert r == l


def test_listtools_flatten_02( ):
   l = [(1, 2), [3, 4]]
   r = listtools.flatten(l)
   assert len(r) == 4
   for e in r:
      assert not isinstance(e, (list, tuple))


def test_listtools_flatten_03( ):
   l = [(1, 2), [3, (4, 5)]]
   r = listtools.flatten(l)
   assert len(r) == 5
   for e in r:
      assert not isinstance(e, (list, tuple))
