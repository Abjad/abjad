from abjad import *


def test_leaftools_duration_rewrite_01( ):
   n = Note(0, (1, 4))
   leaftools.duration_rewrite(n, Rational(3, 16))
   assert n.duration.written == Rational(3, 16)
   assert n.duration.multiplier == Rational(4, 3)
   assert n.duration.prolated == Rational(1, 4)


def test_leaftools_duration_rewrite_02( ):
   n = Note(0, (1, 4))
   leaftools.duration_rewrite(n, Rational(7, 8))
   assert n.duration.written == Rational(7, 8)
   assert n.duration.multiplier == Rational(2, 7)
   assert n.duration.prolated == Rational(1, 4)


def test_leaftools_duration_rewrite_03( ):
   n = Note(0, (1, 4))
   leaftools.duration_rewrite(n, Rational(15, 16))
   assert n.duration.written == Rational(15, 16)
   assert n.duration.multiplier == Rational(4, 15)
   assert n.duration.prolated == Rational(1, 4)
