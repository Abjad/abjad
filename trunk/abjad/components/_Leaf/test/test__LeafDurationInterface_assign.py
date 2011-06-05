from abjad import *
import py.test


def test__LeafDurationInterface_assign_01( ):
   '''Written duration can be assigned a Duration.'''
   t = Note(1, (1, 4))
   t.duration.written = Duration(1, 8)
   assert t.duration.written == Duration(1, 8)


def test__LeafDurationInterface_assign_02( ):
   '''Written duration can be assigned an int.'''
   t = Note(1, (1, 4))
   t.duration.written = 2
   assert t.duration.written == Duration(2, 1)


def test__LeafDurationInterface_assign_03( ):
   '''Written duration can be assigned an tuple.'''
   t = Note(1, (1, 4))
   t.duration.written = (1, 2)
   assert t.duration.written == Duration(1, 2)


def test__LeafDurationInterface_assign_04( ):
   '''Multiplier duration can be assigned a Duration.'''
   t = Note(1, (1, 4))
   t.duration.multiplier = Duration(1, 8)
   assert t.duration.multiplier == Duration(1, 8)


def test__LeafDurationInterface_assign_05( ):
   '''Multiplier duration can be assigned an int.'''
   t = Note(1, (1, 4))
   t.duration.multiplier = 2
   assert t.duration.multiplier == Duration(2, 1)
