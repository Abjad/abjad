from abjad import *


def test_leaf_duration_rewrite_01( ):
   '''Rewriting works against a nonmultiplied duration.'''
   t = Note(0, (1, 4))
   t.duration.rewrite((1, 16))
   assert t.duration.written == Rational(1, 16)
   assert t.duration.multiplier == Rational(4, 1)


def test_leaf_duration_rewrite_02( ):
   '''Rewriting works against a multiplied duration.'''
   t = Note(0, (1, 16))
   t.duration.multiplier = 4
   t.duration.rewrite((1, 4))
   assert t.duration.written == Rational(1, 4)
   assert t.duration.multiplier is None
