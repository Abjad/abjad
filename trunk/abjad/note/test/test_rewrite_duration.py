from abjad import *


def test_rewrite_duration_as_01a( ):
   n = Note(0, (1, 4))
   n.duration.rewrite((3, 16))
   assert n.duration.written == Rational(3, 16)
   assert n.duration.multiplier == Rational(4, 3)
   assert n.duration.prolated == Rational(1, 4)


def test_rewrite_duration_as_01b( ):
   n = Note(0, (1, 4))
   n.duration.rewrite(Rational(3, 16))
   assert n.duration.written == Rational(3, 16)
   assert n.duration.multiplier == Rational(4, 3)
   assert n.duration.prolated == Rational(1, 4)


def test_rewrite_duration_as_01c( ):
   n = Note(0, (1, 4))
   n.duration.rewrite(Rational(3, 16))
   assert n.duration.written == Rational(3, 16)
   assert n.duration.multiplier == Rational(4, 3)
   assert n.duration.prolated == Rational(1, 4)


def test_rewrite_duration_as_02( ):
   n = Note(0, (1, 4))
   n.duration.rewrite((3, 16))
   assert n.duration.written == Rational(3, 16)
   assert n.duration.multiplier == Rational(4, 3)
   assert n.duration.prolated == Rational(1, 4)


def test_rewrite_duration_as_03( ):
   n = Note(0, (1, 4))
   n.duration.rewrite((7, 8))
   assert n.duration.written == Rational(7, 8)
   assert n.duration.multiplier == Rational(2, 7)
   assert n.duration.prolated == Rational(1, 4)


def test_rewrite_duration_as_04( ):
   n = Note(0, (1, 4))
   n.duration.rewrite((15, 16))
   assert n.duration.written == Rational(15, 16)
   assert n.duration.multiplier == Rational(4, 15)
   assert n.duration.prolated == Rational(1, 4)
