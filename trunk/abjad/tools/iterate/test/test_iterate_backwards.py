from abjad import *


def test_iterate_backwards_01( ):
   '''Yield nothing when class not present.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   iter = iterate.backwards(t, Rest)
   assert len(list(iter)) == 0


def test_iterate_backwards_02( ):
   '''Yield topmost node only.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   iter = iterate.backwards(t, Staff)
   assert len(list(iter)) == 1


def test_iterate_backwards_03( ):
   '''Yield internal nodes only.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   from abjad.tuplet.tuplet import _Tuplet
   iter = iterate.backwards(t, _Tuplet)
   assert len(list(iter)) == 3


def test_iterate_backwards_04( ):
   '''Yield exact leaves.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   iter = iterate.backwards(t, Note)
   assert len(list(iter)) == 9


def test_iterate_backwards_05( ):
   '''Yield leaves based on names higher in inheritence hierarchy.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   from abjad.leaf.leaf import _Leaf
   iter = iterate.backwards(t, _Leaf)
   assert len(list(iter)) == 9


def test_iterate_backwards_06( ):
   '''Yield all nodes in tree.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   from abjad.component.component import _Component
   iter = iterate.backwards(t, _Component)
   assert len(list(iter)) == 13


def test_iterate_backwards_07( ):
   '''Yield all all python objects.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   iter = iterate.backwards(t, object)
   assert len(list(iter)) == 13
