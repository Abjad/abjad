from abjad import *


def test_tonalitytools_are_stepwise_ascending_01( ):

   notes = leaftools.make_first_n_notes_in_ascending_diatonic_scale(4)
   staff = Staff(notes)

   assert tonalitytools.are_stepwise_ascending(staff.leaves)


def test_tonalitytools_are_stepwise_ascending_02( ):

   notes = leaftools.make_first_n_notes_in_ascending_diatonic_scale(4)
   notes.reverse( )
   staff = Staff(notes)

   assert not tonalitytools.are_stepwise_ascending(staff.leaves)
