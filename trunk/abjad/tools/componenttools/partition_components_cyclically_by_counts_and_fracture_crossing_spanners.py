from abjad.tools.componenttools._partition_by_counts import _partition_by_counts


def partition_components_cyclically_by_counts_and_fracture_crossing_spanners(components, counts):
   '''Partition container into parts of lengths equal to counts.
      Fracture spanners attaching directly to container.
      Leave spanners attaching to container contents untouched.
      Return Python list of partitioned parts.

   .. versionchanged:: 1.1.2
      renamed ``partition.cyclic_fractured_by_counts( )`` to
      ``componenttools.partition_components_cyclically_by_counts_and_fracture_crossing_spanners( )``.
   '''

   return _partition_by_counts(
      components, counts, spanners = 'fractured', cyclic = True)
