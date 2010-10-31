from fractions import Fraction


def remove_subsequence_of_weight_at_index(sequence, weight, index):
   '''Remove subsequence of `weight` at `index`::

      abjad> seqtools.remove_subsequence_of_weight_at_index((1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6), 13, 4)
      [1, 1, 2, 3, 5, 5, 6]

   Return newly constructed `sequence` type.

   .. versionchanged:: 1.1.2
      renamed ``listtools.remove_weighted_subrun_at( )`` to
      ``seqtools.remove_subsequence_of_weight_at_index( )``.
   '''

   result = list(sequence[:index])
   total = 0
   for element in sequence[index:]:
      if weight <= total:
         result.append(element)
      elif weight < total + element:
         result.append(total + element - weight)
      total += element
   return type(sequence)(result)
