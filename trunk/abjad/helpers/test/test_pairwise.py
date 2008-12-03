from abjad import *


def test_pairwise_01( ):
   '''Pairwise list of numbers.'''
   t = range(6)
   pairs = pairwise(t)
   assert list(pairs) == [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]


def test_pairwise_02( ):
   '''Pairwise list of notes.'''
   t = [Note(x, (1, 4)) for x in range(6)]
   pairs = pairwise(t)
   for i, pair in enumerate(pairs):
      assert (pair[0].signature, pair[1].signature) == \
             (t[i].signature, t[i + 1].signature)
