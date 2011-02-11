import itertools


def partition_sequence_by_value_of_elements(sequence):
   '''Group `sequence` elements by equality::

      abjad> seqtools.partition_sequence_by_value_of_elements([0, 0, -1, -1, 2, 3, -5, 1, 1, 5, -5])
      [(0, 0), (-1, -1), (2,), (3,), (-5,), (1, 1), (5,), (-5,)] 

   Return list of tuples of `sequence` element references.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.group_by_equality( )`` to
      ``seqtools.partition_sequence_by_value_of_elements( )``.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.group_sequence_elements_by_equality( )`` to
      ``seqtools.partition_sequence_by_value_of_elements( )``.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.partition_sequence_by_equality( )`` to
      ``seqtools.partition_sequence_by_value_of_elements( )``.
   '''

   result = [ ]
   g = itertools.groupby(sequence, lambda x: x)
   for n, group in g:
      result.append(tuple(group))
   return result
