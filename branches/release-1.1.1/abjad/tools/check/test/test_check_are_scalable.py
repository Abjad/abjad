from abjad import *


def test_check_are_scalable_01( ):
   t = [Note(0, (1, 8))]
   assert check.are_scalable(t, Rational(1, 2))


def test_check_are_scalable_02( ):
   t = [Note(0, (1, 8))]
   assert check.are_scalable(t, Rational(2, 1))


def test_check_are_scalable_03( ):
   t = [Note(0, (1, 8))]
   assert not check.are_scalable(t, Rational(2, 3))


def test_check_are_scalable_04( ):
   t = [Note(0, (1, 8))]
   assert check.are_scalable(t, Rational(3, 2))


def test_check_are_scalable_05( ):
   t = [Note(0, (3, 16))]
   assert check.are_scalable(t, Rational(2, 3))


def test_check_are_scalable_06( ):
   t = [Note(0, (3, 16))]
   assert not check.are_scalable(t, Rational(3, 2))
