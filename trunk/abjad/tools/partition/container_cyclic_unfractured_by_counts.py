from abjad.container.container import Container
from abjad.tools import split
from abjad.tools.partition._cyclic_by_counts import _cyclic_by_counts as \
   partition__cyclic_by_counts


def container_cyclic_unfractured_by_counts(container, counts):
   '''Partition container into parts of lengths equal to counts.
      Read counts cyclically to determine split points.
      Leave all spanners untouched.
      Return Python list of partitioned parts.'''

   return partition__cyclic_by_counts(
      container, counts, spanners = 'unfractured')
