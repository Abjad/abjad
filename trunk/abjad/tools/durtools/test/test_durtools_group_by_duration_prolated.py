from abjad import *
import py.test


def test_durtools_group_by_duration_prolated_01( ):

   notes = construct.notes(
      [0], [(1, 4), (1, 4), (1, 8), (1, 16), (1, 16), (1, 16)])
   groups = durtools.group_by_duration_prolated(notes)

   assert groups.next( ) == (notes[0], notes[1])
   assert groups.next( ) == (notes[2], )
   assert groups.next( ) == (notes[3], notes[4], notes[5])
   assert py.test.raises(StopIteration, 'groups.next( )') 
