from abjad import *
from py.test import raises


def test_note_compare_01( ):
   '''Notes referentially equal.'''
   n1 = Note(0, (1, 4))
   assert     n1 == n1
   assert not n1 != n1
   assert raises(Exception, 'n1 >  n1')
   assert raises(Exception, 'n1 >= n1')
   assert raises(Exception, 'n1 <  n1')
   assert raises(Exception, 'n1 <= n1')


def test_note_compare_02( ):
   '''Notes superficially similar.'''
   n1 = Note(0, (1, 4))
   n2 = Note(0, (1, 4))
   assert not n1 == n2
   assert     n1 != n2
   assert raises(Exception, 'n1 >  n1')
   assert raises(Exception, 'n1 >= n1')
   assert raises(Exception, 'n1 <  n1')
   assert raises(Exception, 'n1 <= n1')


def test_note_compare_03( ):
   '''Notes manifestly different.'''
   n1 = Note(0, (1, 4))
   n2 = Note(2, (1, 8))
   assert not n1 == n2
   assert     n1 != n2
   assert raises(Exception, 'n1 >  n1')
   assert raises(Exception, 'n1 >= n1')
   assert raises(Exception, 'n1 <  n1')
   assert raises(Exception, 'n1 <= n1')
