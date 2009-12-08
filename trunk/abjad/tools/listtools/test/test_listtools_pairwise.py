from abjad import *


def test_listtools_pairwise_01( ):
   '''Pairwise list of numbers.'''
   t = range(6)
   pairs = listtools.pairwise(t)
   assert list(pairs) == [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]


def test_listtools_pairwise_02( ):
   '''Pairwise list of notes.'''
   t = [Note(x, (1, 4)) for x in range(6)]
   pairs = listtools.pairwise(t)
   for i, pair in enumerate(pairs):
      assert (pair[0].signature, pair[1].signature) == \
             (t[i].signature, t[i + 1].signature)


def test_listtools_pairwise_03( ):
   '''Wrapped pairwise.'''
   t = range(6)
   pairs = listtools.pairwise(t, 'wrap')
   assert list(pairs) == [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]


def test_listtools_pairwise_04( ):
   '''Counted pairwise.'''
   t = range(6)
   pairs = listtools.pairwise(t, 10)
   assert list(pairs) == [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 1), (1, 2), (2, 3), (3, 4)]


def test_listtools_pairwise_05( ):
   '''Cyclic pairwise.'''
   t = range(6)
   pairs = listtools.pairwise(t, 'cycle')
   for x in range(100):
      assert pairs.next( )


def test_listtools_pairwise_06( ): 
   '''Works on generators.'''
   t = xrange(6)
   pairs = listtools.pairwise(t)
   pairs = list(pairs)
   assert pairs[0] == (0, 1)
   assert pairs[1] == (1, 2)
   assert pairs[2] == (2, 3)
   assert pairs[3] == (3, 4)
   assert pairs[4] == (4, 5)
