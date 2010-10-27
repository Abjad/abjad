def iterate_sequence_pairwise_wrapped(sequence):
   '''Iterate `sequence` pairwise wrapped.

   Return pair generator.
   '''

   for i in range(len(sequence)):
      yield (sequence[i], sequence[(i + 1) % len(sequence)])
