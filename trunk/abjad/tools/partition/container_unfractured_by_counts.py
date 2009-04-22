from abjad.tools.partition._by_counts import _by_counts as \
   partition__by_counts


def container_unfractured_by_counts(container, counts):
   '''Partition container into parts of lengths equal to counts.
      Leave all spanners untouched.
      Return Python list of partitioned parts.'''

   return partition__by_counts(container, counts, spanners = 'unfractured')
