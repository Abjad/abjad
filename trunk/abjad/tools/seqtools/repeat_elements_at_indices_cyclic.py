def repeat_elements_at_indices_cyclic(sequence, cycle_token, total):
   '''.. versionadded:: 1.1.2

   Repeat `sequence` elements at indices specified by `cycle_token` to `total` length::

      abjad> t = list(seqtools.repeat_elements_at_indices_cyclic(range(10), (5, [1, 2]), 3))
      [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, [6, 6, 6], [7, 7, 7], 8, 9]

   The `cycle_token` may be a sieve::

      abjad> sieve = sievetools.cycle_tokens_to_sieve((5, [1, 2]))
      abjad> t = list(seqtools.repeat_elements_at_indices_cyclic(range(10), sieve, 3))
      [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, [6, 6, 6], [7, 7, 7], 8, 9]

   Return generator.
   '''
   from abjad.tools import sievetools

   sieve = sievetools.cycle_tokens_to_sieve(cycle_token)
   list_sequence = list(sequence)
   indices = sieve.get_congruent_bases(len(list_sequence))

   for i, element in enumerate(sequence):
      if i in indices:
         yield [element] * total
      else:
         yield element
