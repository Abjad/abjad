from abjad import *


def test_tonalharmony_is_neighbor_note_01( ):

   notes = construct.notes([0, 2, 4, 2, 0], [(1, 4)])
   t = Staff(notes)
   
   assert not tonalharmony.is_neighbor_note(t[0])
   assert not tonalharmony.is_neighbor_note(t[1])
   assert tonalharmony.is_neighbor_note(t[2])
   assert not tonalharmony.is_neighbor_note(t[3])
   assert not tonalharmony.is_neighbor_note(t[4])
