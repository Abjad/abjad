from abjad import *
import py.test


def test_durtools_partition_noncyclic_with_overhang_by_durations_prolated_01( ):

   notes = leaftools.make_notes([0], [(1, 8), (1, 8), (1, 4), (1, 8), (1, 8)])
   parts = durtools.partition_noncyclic_with_overhang_by_durations_prolated(
      notes, [(1, 4)])
      
   assert parts.next( ) == (notes[0], notes[1])
   assert parts.next( ) == (notes[2], notes[3], notes[4])
   assert py.test.raises(StopIteration, 'parts.next( )')


def test_durtools_partition_noncyclic_with_overhang_by_durations_prolated_02( ):

   notes = leaftools.make_notes([0], [(1, 8), (1, 8), (1, 4), (1, 8), (1, 8)])
   parts = durtools.partition_noncyclic_with_overhang_by_durations_prolated(
      notes, [(3, 16)])
      
   assert py.test.raises(PartitionError, 'parts.next( )')
