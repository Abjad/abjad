from abjad.tools.seqtools._split_sequence_by_weights import _split_sequence_by_weights


## NOTE THAT THIS FUNCTION IS REALLY A SPLIT FUNCTION RATHER THAN PARTITION;
## function temporarily reimplemented in terms fo split function;
## function marked for deprecation.
def partition_sequence_by_weights(sequence, weights, cyclic = False, overhang = False):
   '''Partition `sequence` by `weights`.
   
   With one-element ``weights``::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [15])
      [[15]]

   ::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [15], cyclic = True)
      [[15], [5, 10], [10, 5], [15], [15]]

   ::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [15], overhang = True)
      [[15], [5, 20, 20, 20]]

   ::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [15], cyclic = True, overhang = True)
      [[15], [5, 10], [10, 5], [15], [15], [5]]

   With multi-element ``weights``::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [7, 15])
      [[7], [13, 2]]

   ::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [7, 15], cyclic = True)
      [[7], [13, 2], [7], [11, 4], [9, 6], [7]]

   ::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [7, 15], overhang = True)
      [[7], [13, 2], [18, 20, 20]]

   ::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [7, 15], cyclic = True, overhang = True)
      [[7], [13, 2], [7], [11, 4], [7], [9, 6], [7], [7]]

   Because ``mathtools.weight(sequence)`` equals the sum of the absolute
   values of the elements in list `sequence`, negative numbers in `sequence`
   give negative numbers in the output of ``seqtools.partition_sequence_by_weights( )``::

      abjad> seqtools.partition_sequence_by_weights([20, -20, 20, -20], [7, 15], cyclic = True)
      [[7], [13, -2], [-7], [-11, 4], [7], [9, -6], [-7]]

   Set `weights` to any iterable of one or more positive numbers.

   Set `cyclic` to true or false.

   Set `overhang` to true or false.

   Return ``result`` comprising sublists such that ``mathtools.weight(r_i)`` 
   for ``r_i`` in ``result`` equals ``s_i`` for ``s_i`` in list of weights ``s``.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.partition_by_weights( )`` to
      ``seqtools.partition_sequence_by_weights( )``.
   '''

   return _split_sequence_by_weights(sequence, weights, cyclic = cyclic, overhang = overhang)
