from abjad.tools.partition._by_counts import _by_counts


def cyclic_fractured_by_counts(components, counts):
   '''Partition container into parts of lengths equal to counts.
      Fracture spanners attaching directly to container.
      Leave spanners attaching to container contents untouched.
      Return Python list of partitioned parts.
   '''

   return _by_counts(
      components, counts, spanners = 'fractured', cyclic = True)
