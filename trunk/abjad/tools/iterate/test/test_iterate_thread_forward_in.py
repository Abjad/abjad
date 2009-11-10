from abjad import *


def test_iterate_thread_forward_in_01( ):
   '''Yield nothing when class not present.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   iter = iterate.thread_forward_in(t, Rest, t[0].thread.signature)
   assert len(list(iter)) == 0


def test_iterate_thread_forward_in_02( ):
   '''Yield internal nodes only.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   from abjad.tuplet.tuplet import _Tuplet
   iter = iterate.thread_forward_in(t, _Tuplet, t[0].thread.signature)
   assert len(list(iter)) == 3


def test_iterate_thread_forward_in_03( ):
   '''Yield exact leaves.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   iter = iterate.thread_forward_in(t, Note, t[0].thread.signature)
   assert len(list(iter)) == 9


def test_iterate_thread_forward_in_04( ):
   '''Yield leaves based on names higher in inheritence hierarchy.'''
   t = Staff(FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 3)
   from abjad.leaf import _Leaf
   iter = iterate.thread_forward_in(t, _Leaf, t[0][0].thread.signature )
   assert len(list(iter)) == 9


def test_iterate_thread_forward_in_05( ):
   '''Yield Notes in two contiguous Voices with the same name.'''
   v1 = Voice(Note(0, (1, 4)) * 2)
   v2 = Voice(Note(2, (1, 4)) * 2)
   v1.name = v2.name = 'piccolo'
   t = Staff([v1, v2])
   iter = iterate.thread_forward_in(t, Note, t[0].thread.signature )
   iter = list(iter)

   assert len(iter) == 4
   for e in iter:
      assert isinstance(e, Note)


def test_iterate_thread_forward_in_06( ):
   '''Yield only Notes matching the given thread signature.'''
   v1 = Voice(Note(0, (1, 4)) * 2)
   v2 = Voice(Note(2, (1, 4)) * 2)
   t = Staff([v1, v2])
   iter = iterate.thread_forward_in(t, Note, t[0].thread.signature )
   iter = list(iter)

   assert len(iter) == 2
   for e in iter:
      assert isinstance(e, Note)
      assert e.pitch.number == 0


def test_iterate_thread_forward_in_07( ):
   '''Yield only Notes matching the given thread signature.'''
   v1 = Voice(Note(0, (1, 4)) * 2)
   v2 = Voice(Note(2, (1, 4)) * 2)
   v1.name = 'flute'
   v2.name = 'piccolo'
   t = Staff([v1, v2])
   iter = iterate.thread_forward_in(t, Note, t[0].thread.signature )
   iter = list(iter)

   assert len(iter) == 2
   for e in iter:
      assert isinstance(e, Note)
      assert e.pitch.number == 0






