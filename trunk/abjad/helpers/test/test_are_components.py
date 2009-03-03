from abjad.helpers.are_components import _are_components
from abjad import *


def test_are_components_01( ):
   t = scale(4)
   assert _are_components(t)


def test_are_components_02( ):
   t = Staff(scale(4)) * 4
   assert _are_components(t)


def test_are_components_03( ):
   t = range(4)
   assert not _are_components(t)


def test_are_components_04( ):
   t = [ ]
   assert _are_components(t)
