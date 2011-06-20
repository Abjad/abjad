from abjad import *
from abjad.tools import seqtools
import py.test


def test_seqtools_flatten_sequence_01( ):
   l = [1, 2, 3, 4, 5]
   new = seqtools.flatten_sequence(l)
   assert new == [1, 2, 3, 4, 5]


def test_seqtools_flatten_sequence_02( ):
   l = [(1, 2), [3, 4]]
   new = seqtools.flatten_sequence(l)
   assert new == [1, 2, 3, 4]


def test_seqtools_flatten_sequence_03( ):
   l = [(1, 2), [3, (4, 5)]]
   new = seqtools.flatten_sequence(l)
   assert new == [1, 2, 3, 4, 5]


def test_seqtools_flatten_sequence_04( ):
   l = [(1, 2), [3, (4, 5)]]
   new = seqtools.flatten_sequence(l, klasses = (list, ))
   assert new == [(1, 2), 3, (4, 5)]


def test_seqtools_flatten_sequence_05( ):
   l = [(1, 2), [3, (4, 5)]]
   assert py.test.raises(AssertionError, 'seqtools.flatten_sequence(l, klasses = (tuple, ))')


def test_seqtools_flatten_sequence_06( ):
   l = [1, [2, 3, [4]], 5, [6, 7, [8]]]
   assert seqtools.flatten_sequence(l, depth = 0) == [1, [2, 3, [4]], 5, [6, 7, [8]]]
   assert seqtools.flatten_sequence(l, depth = 1) == [1, 2, 3, [4], 5, 6, 7, [8]]
   assert seqtools.flatten_sequence(l, depth = 2) == [1, 2, 3, 4, 5, 6, 7, 8]
   assert seqtools.flatten_sequence(l, depth = 2) == seqtools.flatten_sequence(l, depth = 99)
