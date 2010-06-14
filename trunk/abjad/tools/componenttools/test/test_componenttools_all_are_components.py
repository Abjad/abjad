from abjad import *


def test_componenttools_all_are_components_01( ):
   t = leaftools.make_first_n_notes_in_ascending_diatonic_scale(4)
   assert componenttools.all_are_components(t)


def test_componenttools_all_are_components_02( ):
   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4)) * 4
   assert componenttools.all_are_components(t)


def test_componenttools_all_are_components_03( ):
   t = range(4)
   assert not componenttools.all_are_components(t)


def test_componenttools_all_are_components_04( ):
   t = [ ]
   assert componenttools.all_are_components(t)
