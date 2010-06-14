from abjad import *
import py.test


def test_durtools_partition_noncyclic_with_overhang_by_durations_prolated_not_less_than_01( ):

   notes = leaftools.make_notes([0], [(1, 8), (1, 8), (1, 4), (1, 8), (1, 8)])
   parts = durtools.partition_noncyclic_with_overhang_by_durations_prolated_not_less_than(notes, [(5, 16)])
      
   assert parts.next( ) == (notes[0], notes[1], notes[2])
   assert parts.next( ) == (notes[3], notes[4])
   assert py.test.raises(StopIteration, 'parts.next( )')


def test_durtools_partition_noncyclic_with_overhang_by_durations_prolated_not_less_than_02( ):
   '''Huge partition size boundary case.'''

   notes = leaftools.make_notes([0], [(1, 8), (1, 8), (1, 4), (1, 8), (1, 8)])
   parts = durtools.partition_noncyclic_with_overhang_by_durations_prolated_not_less_than(notes, [(99, 16)])
      
   assert parts.next( ) == tuple(notes)
   assert py.test.raises(StopIteration, 'parts.next( )')
