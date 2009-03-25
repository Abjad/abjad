from abjad import *


def test_leaf_duration_scale_01( ):
   t = Note(0, (1, 4))
   leaf_duration_scale(t, Rational(1, 2))
   assert t.duration.written == Rational(1, 8)


def test_leaf_duration_scale_02( ):
   t = Note(0, (1, 4))
   leaf_duration_scale(t, Rational(2))
   assert t.duration.written == Rational(1, 2)


def test_leaf_duration_scale_03( ):
   t = Note(0, (1, 4))
   leaf_duration_scale(t, Rational(5, 4))
   assert t.tie.spanner.duration.written == Rational(5, 16)


def test_leaf_duration_scale_04( ):
   t = Note(0, (1, 4))
   leaf_duration_scale(t, Rational(2, 3))
   assert t.duration.written == Rational(1, 4)
   assert t.duration.prolated == Rational(1, 6)
