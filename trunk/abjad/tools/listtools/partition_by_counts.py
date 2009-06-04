from abjad.tools.listtools.pairwise_cumulative_sums import \
   pairwise_cumulative_sums as listtools_pairwise_cumulative_sums
from abjad.tools.listtools.repeat_to_weight import repeat_to_weight as \
   listtools_repeat_to_weight
from abjad.tools.listtools.weight import weight as listtools_weight
from abjad.tools import mathtools


def partition_by_counts(l, s, cyclic = False, overhang = False):
   '''Partition list ``l`` into sublists of such that \
   ``len(r)_i`` for ``r_i`` in ``result`` equals ``s_i``.

   ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      abjad> listtools.partition_by_counts(l, [3])
      [[0, 1, 2]]

   When ``cyclic = True`` repeat the elements in ``s``.

   ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      abjad> listtools.partition_by_counts(l, [3], cyclic = True) 
      [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

   When ``overhang = True`` return any remaining unicorporated \
   elements of ``l`` as a final part in ``result``.

   ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      abjad> listtools.partition_by_counts(l, [3], overhang = True)
      [[0, 1, 2], [3, 4, 5, 6, 7, 8, 9]]

   When both ``cyclic = True`` and ``overhang = True`` repeat the \
   elements in ``s`` and return any remaining unincorporated \
   elements of ``l`` as a final part in ``result``.

   ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      abjad> listtools.partition_by_counts(
         l, [3], cyclic = True, overhang = True)
      [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

   Examples with ``1 < len(s)``.

   ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
      abjad> listtools.partition_by_counts(l, [4, 3])
      [[0, 1, 2, 3], [4, 5, 6]]

   ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
      abjad> listtools.partition_by_counts(l, [4, 3], cyclic = True)
      [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13]]

   ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
      abjad> listtools.partition_by_counts(l, [4, 3], overhang = True)
      [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10, 11, 12, 13, 14, 15]]

   ::

      abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
      abjad> listtools.partition_by_counts(
         l, [4, 3], cyclic = True, overhang = True)
      [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10], [11, 12, 13], [14, 15]]'''

   assert isinstance(s, list)
   assert all([isinstance(x, (int, long)) for x in s])

   result = [ ]

   if cyclic == True:
      if overhang == True:
         s = listtools_repeat_to_weight(s, len(l))
      else:
         s = listtools_repeat_to_weight(s, len(l), remainder = 'less')
   elif overhang == True:
      weight_s = listtools_weight(s)
      len_l = len(l)
      if weight_s < len_l:
         s.append(len(l) - weight_s)

   for start, stop in listtools_pairwise_cumulative_sums(s):
      result.append(l[start:stop])

   return result
