from abjad.tools.seqtools._partition_list_by_counts import _partition_list_by_counts


def partition_sequence_cyclically_by_counts_without_overhang(l, counts):
   '''Partition list `l` cyclically by `counts` without overhang::

      abjad> l = range(16)
      abjad> l 
      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
      
   ::
      
      abjad> seqtools.partition_sequence_cyclically_by_counts_without_overhang(l, [4, 6]) 
      [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13]]

   Return list of lists.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.partition_list_cyclically_by_counts_without_overhang( )`` to
      ``seqtools.partition_sequence_cyclically_by_counts_without_overhang( )``.
   '''

   return _partition_list_by_counts(l, counts, cyclic = True, overhang = False)
