from abjad import *


def test_are_scalable_components_01( ):
   t = [Note(0, (1, 8))]
   assert are_scalable_components(t, Rational(1, 2))


def test_are_scalable_components_02( ):
   t = [Note(0, (1, 8))]
   assert are_scalable_components(t, Rational(2, 1))


def test_are_scalable_components_03( ):
   t = [Note(0, (1, 8))]
   assert not are_scalable_components(t, Rational(2, 3))


def test_are_scalable_components_04( ):
   t = [Note(0, (1, 8))]
   assert are_scalable_components(t, Rational(3, 2))


def test_are_scalable_components_05( ):
   t = [Note(0, (3, 16))]
   assert are_scalable_components(t, Rational(2, 3))


def test_are_scalable_components_06( ):
   t = [Note(0, (3, 16))]
   assert not are_scalable_components(t, Rational(3, 2))
