from abjad.helpers.are_scalable_components import _are_scalable_components
from abjad import *


def test_are_scalable_components_01( ):
   t = [Note(0, (1, 8))]
   assert _are_scalable_components(t, Rational(1, 2))


def test_are_scalable_components_02( ):
   t = [Note(0, (1, 8))]
   assert _are_scalable_components(t, Rational(2, 1))


def test_are_scalable_components_03( ):
   t = [Note(0, (1, 8))]
   assert not _are_scalable_components(t, Rational(2, 3))


def test_are_scalable_components_04( ):
   t = [Note(0, (1, 8))]
   assert _are_scalable_components(t, Rational(3, 2))


def test_are_scalable_components_05( ):
   t = [Note(0, (3, 16))]
   assert _are_scalable_components(t, Rational(2, 3))


def test_are_scalable_components_06( ):
   t = [Note(0, (3, 16))]
   assert not _are_scalable_components(t, Rational(3, 2))
