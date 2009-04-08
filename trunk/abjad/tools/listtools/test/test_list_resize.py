from abjad import *
from py.test import raises


def test_listtools_resize_01( ):
   '''List must not be empty.'''
   assert raises(AssertionError, 'listtools.resize([ ], 2)')


def test_listtools_resize_02( ):
   '''Resize can shrink a list.'''
   t = listtools.resize([1,2,3], 2)
   assert t == [1, 2]


def test_listtools_resize_03( ):
   '''Resize can augment a list.'''
   t = listtools.resize([1,2,3], 8)
   assert t == [1, 2, 3, 1, 2, 3, 1, 2]


def test_listtools_resize_04( ):
   '''Resize can leave list unchanged.'''
   t = listtools.resize([1,2,3], 3)
   assert t == [1, 2, 3]
