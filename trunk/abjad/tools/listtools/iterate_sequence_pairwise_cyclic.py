def iterate_sequence_pairwise_cyclic(sequence):
   '''Iterate `sequence` pairwise cyclic.

   Return pair generator.
   '''

   i = 0
   while True:
      yield (sequence[i % len(sequence)], sequence[(i + 1) % len(sequence)])
      i += 1
