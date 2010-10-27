def repeat_elements_at_indices_cyclic(iterable, cycle_token, total):
   '''.. versionadded:: 1.1.2

   Yield elements in `iterable`, repeating those at indices 
   specified by `cycle_token` to `total` length. ::

      abjad> t = list(seqtools.repeat_elements_at_indices_cyclic(range(10), (5, [1, 2]), 3))
      [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, [6, 6, 6], [7, 7, 7], 8, 9]

   Cycle token may be a sieve. ::

      abjad> sieve = sievetools.cycle_tokens_to_sieve((5, [1, 2]))
      abjad> t = list(seqtools.repeat_elements_at_indices_cyclic(range(10), sieve, 3))
      [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, [6, 6, 6], [7, 7, 7], 8, 9]
   '''

   from abjad.tools import sievetools

   sieve = sievetools.cycle_tokens_to_sieve(cycle_token)
   list_iterable = list(iterable)
   indices = sieve.get_congruent_bases(len(list_iterable))

   for i, element in enumerate(iterable):
      if i in indices:
         yield [element] * total
      else:
         yield element
