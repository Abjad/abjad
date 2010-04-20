from abjad import *


def test_tonalharmony_are_stepwise_descending_01( ):

   notes = construct.scale(4)
   staff = Staff(notes)

   assert not tonalharmony.are_stepwise_descending(staff.leaves)


def test_tonalharmony_are_stepwise_descending_02( ):

   notes = construct.scale(4)
   notes.reverse( )
   staff = Staff(notes)

   assert tonalharmony.are_stepwise_descending(staff.leaves)
