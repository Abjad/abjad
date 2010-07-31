from abjad import *
from py.test import raises


def test_Chord_numbers_01( ):
   '''Returns sorted immutable tuple of numbers in chord.'''
   t = Chord([2, 4, 5], (1, 4))
   numbers = t.numbers
   assert isinstance(numbers, tuple)
   assert len(numbers) == 3
   assert raises(AttributeError, 'numbers.pop( )')
   ## Python 2.6 implements tuple.index( )
   #assert raises(AttributeError, 'numbers.index(numbers[0])')
   assert raises(AttributeError, 'numbers.remove(numbers[0])')


def test_Chord_numbers_02( ):
   '''Chords with equivalent numbers do carry equivalent numbers tuples.'''
   t1 = Chord([2, 4, 5], (1, 4))
   t2 = Chord([2, 4, 5], (1, 4))
   assert t1.numbers == t2.numbers
