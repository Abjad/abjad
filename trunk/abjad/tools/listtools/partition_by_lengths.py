from abjad.tools.listtools.pairwise_cumulative_sums_zero import \
   pairwise_cumulative_sums_zero
from abjad.tools.listtools.repeat_list_to_weight import \
   repeat_list_to_weight
from abjad.tools.listtools.weight import weight
from abjad.tools import mathtools


def partition_by_lengths(l, lengths, cyclic = False, overhang = False):
   '''Partition list `l` into sublists ``r_i`` in ``result`` list 
   such that ``len(r)_i == lengths_i`` for all ``i < len(result)``.

   Input:

   * `l`: any iterable of positive, negative or zero-valued numbers.
   * `lengths`: any iterable of one or more positive integers.
   * `cyclic`: boolean.
   * `overhang`: boolean.

   Output: Python list of one or more sublists. ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      abjad> listtools.partition_by_lengths(l, [3])
      [[0, 1, 2]]

   When ``cyclic = True`` repeat the elements in `lengths`. ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      abjad> listtools.partition_by_lengths(l, [3], cyclic = True) 
      [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

   When ``overhang = True`` return any remaining unicorporated
   elements of `l` as a final part in ``result``. ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      abjad> listtools.partition_by_lengths(l, [3], overhang = True)
      [[0, 1, 2], [3, 4, 5, 6, 7, 8, 9]]

   When both ``cyclic = True`` and ``overhang = True`` repeat the 
   elements in `lengths` and return any remaining unincorporated 
   elements of `l` as a final part in ``result``. ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      abjad> listtools.partition_by_lengths(l, [3], cyclic = True, overhang = True)
      [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

   Examples with ``1 < len(lengths)``. ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
      abjad> listtools.partition_by_lengths(l, [4, 3])
      [[0, 1, 2, 3], [4, 5, 6]]

   ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
      abjad> listtools.partition_by_lengths(l, [4, 3], cyclic = True)
      [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13]]

   ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
      abjad> listtools.partition_by_lengths(l, [4, 3], overhang = True)
      [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10, 11, 12, 13, 14, 15]]

   ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
      abjad> listtools.partition_by_lengths(
         l, [4, 3], cyclic = True, overhang = True)
      [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13], [14, 15]]
   '''

   assert all([isinstance(x, (int, long)) for x in lengths])
   ## TODO: Document boundary case change with examples and tests. ##
   #assert all([0 < x for x in lengths])
   assert all([0 <= x for x in lengths])

   result = [ ]

   if cyclic == True:
      if overhang == True:
         lengths = repeat_list_to_weight(lengths, len(l))
      else:
         lengths = repeat_list_to_weight(lengths, len(l), remainder = 'less')
   elif overhang == True:
      weight_lengths = weight(lengths)
      len_l = len(l)
      if weight_lengths < len_l:
         lengths.append(len(l) - weight_lengths)

   for start, stop in pairwise_cumulative_sums_zero(lengths):
      result.append(l[start:stop])

   return result
