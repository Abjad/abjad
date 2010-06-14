from abjad import *


def test_tonalharmony_are_stepwise_ascending_01( ):

   notes = leaftools.make_first_n_notes_in_ascending_diatonic_scale(4)
   staff = Staff(notes)

   assert tonalharmony.are_stepwise_ascending(staff.leaves)


def test_tonalharmony_are_stepwise_ascending_02( ):

   notes = leaftools.make_first_n_notes_in_ascending_diatonic_scale(4)
   notes.reverse( )
   staff = Staff(notes)

   assert not tonalharmony.are_stepwise_ascending(staff.leaves)
