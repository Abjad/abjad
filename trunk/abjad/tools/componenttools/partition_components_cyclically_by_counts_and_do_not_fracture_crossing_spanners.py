from abjad.tools.partition._by_counts import _by_counts


def partition_components_cyclically_by_counts_and_do_not_fracture_crossing_spanners(components, counts):
   '''Partition container into parts of lengths equal to counts.
      Read counts ally to determine split points.
      Leave all spanners untouched.
      Return Python list of partitioned parts.

   .. versionchanged:: 1.1.2
      renamed ``partition.cyclic_unfractured_by_counts( )`` to
      ``componenttools.partition_components_cyclically_by_counts_and_do_not_fracture_crossing_spanners( )``.
   '''

   return _by_counts(
      components, counts, spanners = 'unfractured', cyclic = True)
