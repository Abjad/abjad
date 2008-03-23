from abjad import *
from py.test import raises


def test_fdtuplet_trim_01( ):
   '''1-element index.'''
   t = FixedDurationTuplet((2, 4), Note(0, (1, 8)) * 3)
   for i, leaf in enumerate(t.leaves):
      leaf.pitch = i
   t.trim(0)
   assert len(t) == 2
   assert t[0].pitch.number == 1
   assert t[1].pitch.number == 2


def test_fdtuplet_trim_02( ):
   '''1-element index.'''
   t = FixedDurationTuplet((2, 4), Note(0, (1, 8)) * 3)
   for i, leaf in enumerate(t.leaves):
      leaf.pitch = i
   t.trim(1)
   assert len(t) == 2
   assert t[0].pitch.number == 0
   assert t[1].pitch.number == 2


def test_fdtuplet_trim_03( ):
   '''1-element index.'''
   t = FixedDurationTuplet((2, 4), Note(0, (1, 8)) * 3)
   for i, leaf in enumerate(t.leaves):
      leaf.pitch = i
   t.trim(2)
   assert len(t) == 2
   assert t[0].pitch.number == 0
   assert t[1].pitch.number == 1


def test_fdtuplet_trim_04( ):
   '''Raises IndexError.'''
   t = FixedDurationTuplet((2, 4), Note(0, (1, 8)) * 3)
   for i, leaf in enumerate(t.leaves):
      leaf.pitch = i
   assert raises(IndexError, 't.trim(3)')


def test_fdtuplet_trim_05( ):
   '''0-element slice.'''
   t = FixedDurationTuplet((2, 4), Note(0, (1, 8)) * 3)
   for i, leaf in enumerate(t.leaves):
      leaf.pitch = i
   t.trim(0, 0)
   assert len(t) == 3
   assert t[0].pitch.number == 0
   assert t[1].pitch.number == 1
   assert t[2].pitch.number == 2


def test_fdtuplet_trim_06( ):
   '''1-element slice.'''
   t = FixedDurationTuplet((2, 4), Note(0, (1, 8)) * 3)
   for i, leaf in enumerate(t.leaves):
      leaf.pitch = i
   t.trim(0, 1)
   assert len(t) == 2
   assert t[0].pitch.number == 1
   assert t[1].pitch.number == 2


def test_fdtuplet_trim_07( ):
   '''1-element slice.'''
   t = FixedDurationTuplet((2, 4), Note(0, (1, 8)) * 3)
   for i, leaf in enumerate(t.leaves):
      leaf.pitch = i
   t.trim(1, 2)
   assert len(t) == 2
   assert t[0].pitch.number == 0
   assert t[1].pitch.number == 2


def test_fdtuplet_trim_08( ):
   '''1-element slice.'''
   t = FixedDurationTuplet((2, 4), Note(0, (1, 8)) * 3)
   for i, leaf in enumerate(t.leaves):
      leaf.pitch = i
   t.trim(2, 3)
   assert len(t) == 2
   assert t[0].pitch.number == 0
   assert t[1].pitch.number == 1


def test_fdtuplet_trim_09( ):
   '''Trimming all leaves raises an exception.'''
   t = FixedDurationTuplet((2, 4), Note(0, (1, 8)) * 3)
   for i, leaf in enumerate(t.leaves):
      leaf.pitch = i
   raises(AssertionError, 't.trim(0, 100)')
