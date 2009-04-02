from abjad import *
from abjad.helpers.leaf_scale import leaf_scale


def test_leaf_scale_01( ):
   '''Identity.'''
   t = Note(0, (1, 4))
   leaf_scale(Rational(1, 4), t)
   assert isinstance(t, Note)
   assert t.duration.written == Rational(1, 4)


def test_leaf_scale_02( ):
   '''Binary augmentation.'''
   t = Note(0, (1, 8))
   leaf_scale(Rational(1, 4), t)
   assert isinstance(t, Note)
   assert t.duration.written == Rational(1, 4)


def test_leaf_scale_03( ):
   '''Binary diminution.'''
   t = Note(0, (1, 2))
   leaf_scale(Rational(1, 4), t)
   assert isinstance(t, Note)
   assert t.duration.written == Rational(1, 4)


def test_leaf_scale_04( ):
   '''Target features nonbinary denominator;
      written duration of source needn't change.'''
   t = Note(0, (1, 4))
   new = leaf_scale(Rational(1, 3), t)
   assert isinstance(new, FixedDurationTuplet)
   assert t.duration.written == Rational(1, 4)
   assert t.duration.prolated == Rational(1, 3)


def test_leaf_scale_05( ):
   '''Target features nonbinary denominator;
      written duration of source must increase (double).'''
   t = Note(0, (1, 8))
   new = leaf_scale(Rational(1, 3), t)
   assert isinstance(new, FixedDurationTuplet)
   assert t.duration.written == Rational(1, 4)
   assert t.duration.prolated == Rational(1, 3)


def test_leaf_scale_06( ):
   '''Target features nonbinary denominator;
      written duration of source must decrease (half). '''
   t = Note(0, (1, 2))
   new = leaf_scale(Rational(1, 3), t)
   assert isinstance(new, FixedDurationTuplet)
   assert t.duration.written == Rational(1, 2)
   assert t.duration.prolated == Rational(1, 3)


def test_leaf_scale_07( ):
   '''t-numerator in target duration; 
      written duration of source needn't scale.'''
   t = Note(0, (1, 2))
   new = leaf_scale(Rational(5, 8), t)
   assert isinstance(new, FixedDurationTuplet)
   assert t.duration.written == Rational(1, 2)
   assert t.duration.prolated == Rational(5, 8)


def test_leaf_scale_08( ):
   '''t-numerator in target duration; 
      written duration of source must increase (duble).'''
   t = Note(0, (1, 4))
   new = leaf_scale(Rational(5, 8), t)
   assert isinstance(new, FixedDurationTuplet)
   assert t.duration.written == Rational(1, 2)
   assert t.duration.prolated == Rational(5, 8)


def test_leaf_scale_09( ):
   '''t-numerator in target duration; 
      written duration of source must decrease.'''
   t = Note(0, (3, 2))
   new = leaf_scale(Rational(5, 8), t)
   assert isinstance(new, FixedDurationTuplet)
   assert t.duration.written == Rational(1, 1)
   assert t.duration.prolated == Rational(5, 8)


def test_leaf_scale_10( ):
   '''t-numerator in target duration; 
      target features non-binary denominator.
      written duration of source needn't change.'''
   t = Note(0, (1, 2))
   new = leaf_scale(Rational(5, 7), t)
   assert isinstance(new, FixedDurationTuplet) 
   assert t.duration.written == Rational(1, 2)
   assert t.duration.prolated == Rational(5, 7)


def test_leaf_scale_11( ):
   '''t-numerator in target duration;
      target features non-binary denominator.
      written duration of source increases (doubles).'''
   t = Note(0, (1, 4))
   new = leaf_scale(Rational(5, 7), t)
   assert isinstance(new, FixedDurationTuplet) 
   assert t.duration.written == Rational(1, 2)
   assert t.duration.prolated == Rational(5, 7)


def test_leaf_scale_12( ):
   '''t-numerator in target duration;
      target features non-binary denominator.
      written duration of source decreases.'''
   t = Note(0, (3, 2))
   new = leaf_scale(Rational(5, 7), t)
   assert isinstance(new, FixedDurationTuplet) 
   assert t.duration.written == Rational(1, 1)
   assert t.duration.prolated == Rational(5, 7)
