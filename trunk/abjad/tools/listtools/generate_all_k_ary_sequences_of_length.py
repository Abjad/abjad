from abjad.tools import mathtools


def generate_all_k_ary_sequences_of_length(k, length):
   '''.. versionadded:: 1.1.2

   Generate all `k`-ary sequences of `length`::

      abjad> for sequence in listtools.generate_all_k_ary_sequences_of_length(2, 3):
      ...     sequence
      ... 
      (0, 0, 0)
      (0, 0, 1)
      (0, 1, 0)
      (0, 1, 1)
      (1, 0, 0)
      (1, 0, 1)
      (1, 1, 0)
      (1, 1, 1)

   Return generator.
   '''

   assert isinstance(k, int) and 1 <= k
   assert isinstance(length, int) and 0 <= length

   total_sequences = k ** length
   for rank in range(total_sequences):
      result = list(mathtools.integer_to_base_k_tuple(rank, k))
      n_leading_zeros = length - len(result)
      leading_zeros = n_leading_zeros * [0]
      result[0:0] = leading_zeros
      yield tuple(result)
