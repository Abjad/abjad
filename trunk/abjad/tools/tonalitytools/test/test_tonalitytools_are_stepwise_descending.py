from abjad import *


def test_tonalitytools_are_stepwise_descending_01( ):

   notes = macros.scale(4)
   staff = Staff(notes)

   assert not tonalitytools.are_stepwise_descending(staff.leaves)


def test_tonalitytools_are_stepwise_descending_02( ):

   notes = macros.scale(4)
   notes.reverse( )
   staff = Staff(notes)

   assert tonalitytools.are_stepwise_descending(staff.leaves)
