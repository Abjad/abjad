from abjad.tools.partition._by_counts import _by_counts as \
   partition__by_counts


def cyclic_unfractured_by_counts(components, counts):
   '''Partition container into parts of lengths equal to counts.
      Read counts ally to determine split points.
      Leave all spanners untouched.
      Return Python list of partitioned parts.'''

   return partition__by_counts(
      components, counts, spanners = 'unfractured', cyclic = True)
