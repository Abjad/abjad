from abjad.helpers.resize_list import _resize_list
from py.test import raises

def test_resize_list_01( ):
   '''List must not be empty.'''
   assert raises(AssertionError, '_resize_list([ ], 2)')


def test_resize_list_02( ):
   '''Resize can shrink a list.'''
   t = _resize_list([1,2,3], 2)
   assert t == [1, 2]


def test_resize_list_03( ):
   '''Resize can augment a list.'''
   t = _resize_list([1,2,3], 8)
   assert t == [1, 2, 3, 1, 2, 3, 1, 2]


def test_resize_list_04( ):
   '''Resize can leave list unchanged.'''
   t = _resize_list([1,2,3], 3)
   assert t == [1, 2, 3]



