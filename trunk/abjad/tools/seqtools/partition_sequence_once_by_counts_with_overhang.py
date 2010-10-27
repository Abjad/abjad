from abjad.tools.seqtools._partition_list_by_counts import _partition_list_by_counts


def partition_sequence_once_by_counts_with_overhang(l, counts):
   '''Partition list `l` once by `counts` with overhang::

      abjad> l = range(16)
      abjad> l 
      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
      
   ::
      
      abjad> seqtools.partition_sequence_once_by_counts_with_overhang(l, [4, 6]) 
      [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15]]

   Return list of lists.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.partition_list_once_by_counts_with_overhang( )`` to
      ``seqtools.partition_sequence_once_by_counts_with_overhang( )``.
   '''

   return _partition_list_by_counts(l, counts, cyclic = False, overhang = True)
