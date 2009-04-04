from abjad import *
import py.test

def test_assess_are_contexts_01( ):
   '''argument must be a list.'''
   py.test.raises(TypeError, 'assess_are_contexts(123)')


def test_assess_are_contexts_02( ):
   '''Returns True only when ALL elements in list are contexts.'''
   assert not assess_are_contexts([1, 2, 4])
   assert not assess_are_contexts(run(8))
   assert assess_are_contexts(Voice(run(2)) * 2)


def test_assess_are_contexts_03( ):
   '''Returns True on empty list.'''
   assert assess_are_contexts([ ])

