from abjad import *
import py.test


def test_listtools_repeat_to_length_01( ):
   '''Repeat list to length.'''

   l = range(5)
   t = listtools.repeat_to_length(l, 11)

   assert t == [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]


def test_listtools_repeat_to_length_02( ):
   '''Repeat list to length.'''

   l = [0, -1, -2, -3, -4]
   t = listtools.repeat_to_length(l, 11)

   assert t == [0, -1, -2, -3, -4, 0, -1, -2, -3, -4, 0]


def test_listtools_repeat_to_length_03( ):
   '''When length is less than length of list
      return only the first length elements of list.'''

   l = [0, 1, 2, 3, 4]
   t = listtools.repeat_to_length(l, 3)

   assert t == [0, 1, 2]


def test_listtools_repeat_to_length_04( ):
   '''When length is zero return an empty list.'''

   l = [0, 1, 2, 3, 4]
   t = listtools.repeat_to_length(l, 0)

   assert t == [ ]


def test_listtools_repeat_to_length_05( ):
   '''List must not be empty.'''
   assert py.test.raises(AssertionError, 'listtools.repeat_to_length([ ], 2)')


def test_listtools_repeat_to_length_06( ):
   '''Can shrink a list.'''
   t = listtools.repeat_to_length([1, 2, 3], 2)
   assert t == [1, 2]


def test_listtools_repeat_to_length_07( ):
   '''Can augment a list.'''
   t = listtools.repeat_to_length([1, 2, 3], 8)
   assert t == [1, 2, 3, 1, 2, 3, 1, 2]


def test_listtools_repeat_to_length_08( ):
   '''Can leave list unchanged.'''
   t = listtools.repeat_to_length([1, 2, 3], 3)
   assert t == [1, 2, 3]
