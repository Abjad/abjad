from abjad import *


def test_componenttools_all_are_components_01( ):
   t = macros.scale(4)
   assert componenttools.all_are_components(t)


def test_componenttools_all_are_components_02( ):
   t = Staff(macros.scale(4)) * 4
   assert componenttools.all_are_components(t)


def test_componenttools_all_are_components_03( ):
   t = range(4)
   assert not componenttools.all_are_components(t)


def test_componenttools_all_are_components_04( ):
   t = [ ]
   assert componenttools.all_are_components(t)
