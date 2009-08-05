from abjad import *
from py.test import raises


def test_note_compare_01( ):
   '''Chords referentially equal.'''
   ch1 = Chord([2, 4, 5], (1, 4))
   assert     ch1 == ch1
   assert not ch1 != ch1
   assert raises(Exception, 'ch1 >  ch1')
   assert raises(Exception, 'ch1 >= ch1')
   assert raises(Exception, 'ch1 <  ch1')
   assert raises(Exception, 'ch1 <= ch1')


def test_note_compare_02( ):
   '''Chords superficially similar.'''
   ch1 = Chord([2, 4, 5], (1, 4))
   ch2 = Chord([2, 4, 5], (1, 4))
   assert not ch1 == ch2
   assert     ch1 != ch2
   assert raises(Exception, 'ch1 >  ch1')
   assert raises(Exception, 'ch1 >= ch1')
   assert raises(Exception, 'ch1 <  ch1')
   assert raises(Exception, 'ch1 <= ch1')


def test_note_compare_03( ):
   '''Chords manifestly different.'''
   ch1 = Chord([2, 4, 5], (1, 4))
   ch2 = Chord([6, 7, 9], (1, 8))
   assert not ch1 == ch2
   assert     ch1 != ch2
   assert raises(Exception, 'ch1 >  ch1')
   assert raises(Exception, 'ch1 >= ch1')
   assert raises(Exception, 'ch1 <  ch1')
   assert raises(Exception, 'ch1 <= ch1')
