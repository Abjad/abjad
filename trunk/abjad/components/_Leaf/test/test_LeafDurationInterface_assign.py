from abjad import *
import py.test


def test_LeafDurationInterface_assign_01( ):
   '''Written duration can be assigned a Rational.'''
   t = Note(1, (1, 4))
   t.duration.written = Rational(1, 8)
   assert t.duration.written == Rational(1, 8)


def test_LeafDurationInterface_assign_02( ):
   '''Written duration can be assigned an int.'''
   t = Note(1, (1, 4))
   t.duration.written = 2
   assert t.duration.written == Rational(2, 1)


def test_LeafDurationInterface_assign_03( ):
   '''Written duration can NOT be assigned an tuple.'''
   t = Note(1, (1, 4))
   py.test.raises(ValueError, 't.duration.written = (1, 2)')


def test_LeafDurationInterface_assign_04( ):
   '''Multiplier duration can be assigned a Rational.'''
   t = Note(1, (1, 4))
   t.duration.multiplier = Rational(1, 8)
   assert t.duration.multiplier == Rational(1, 8)


def test_LeafDurationInterface_assign_05( ):
   '''Multiplier duration can be assigned an int.'''
   t = Note(1, (1, 4))
   t.duration.multiplier = 2
   assert t.duration.multiplier == Rational(2, 1)
