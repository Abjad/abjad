from abjad import *


def test__LeafDurationInterface_compare_01( ):
   '''Written Durations can be evaluated for equality with Durations.'''
   t = Note("c'4")
   assert t.duration.written == Duration(1, 4)


def test__LeafDurationInterface_compare_02( ):
   '''Written Durations can be evaluated for equality with integers.'''
   t = Note(0, 1)
   assert t.duration.written == 1


def test__LeafDurationInterface_compare_03( ):
   '''Written Durations can NOT be evaluated for equality with tuples.'''
   t = Note("c'4")
   assert t.duration.written == Duration(1, 4)
   assert t.duration.written != (1, 4)
   assert t.duration.written != 'foo'


def test__LeafDurationInterface_compare_04( ):
   '''Multiplier Durations can be evaluated for equality with Durations.'''
   t = Note(1, (1, 4))
   t.duration_multiplier = Duration(1, 4)
   assert t.duration_multiplier == Duration(1, 4)


def test__LeafDurationInterface_compare_05( ):
   '''Multiplier Durations can be evaluated for equality with integers.'''
   t = Note(1, 4)
   t.duration_multiplier = Duration(1)
   assert t.duration_multiplier == Duration(1)
   assert t.duration_multiplier == 1
   assert t.duration_multiplier != (1, 1)
   assert t.duration_multiplier != 'foo'


def test__LeafDurationInterface_compare_06( ):
   '''Multiplier durations compare unequally with 
      all values other than Durations.'''
   t = Note("c'4")
   t.duration_multiplier = Duration(1, 8)
   assert t.duration_multiplier == Duration(1, 8)
   assert t.duration_multiplier != (1, 8)
   assert t.duration_multiplier != 'foo'
