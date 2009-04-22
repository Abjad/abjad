from abjad.tools.partition._cyclic_by_counts import _cyclic_by_counts as \
   partition__cyclic_by_counts


def container_cyclic_fractured_by_counts(container, counts):
   '''Partition container into parts of lengths equal to counts.
      Fracture spanners attaching directly to container.
      Leave spanners attaching to container contents untouched.
      Return Python list of partitioned parts.'''

   return partition__cyclic_by_counts(container, counts, spanners = 'fractured')
