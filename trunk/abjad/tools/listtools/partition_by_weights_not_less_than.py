from abjad.tools import mathtools
from abjad.tools.listtools.weight import weight as listtools_weight


def partition_by_weights_not_less_than(
   l, weights, cyclic = False, overhang = False):
   r'''.. versionadded:: 1.1.2

   Partition `l` into sublists ``result[0], ..., result[n]`` such that
   ``weights[i] <= listtools.weight(result[i])``. ::

      abjad> l = range(10)
      abjad> listtools.partition_by_weights_not_less_than(l, [3])
      [[0, 1, 2]]

   ::

      abjad> listtools.partition_by_weights_not_less_than(l, [10])
      [[0, 1, 2, 3, 4]]

   ::

      abjad> listtools.partition_by_weights_not_less_than(l, [3, 10])
      [[0, 1, 2], [3, 4, 5]]

   When `cyclic` is true, partition `l` such that
   ``weights[i%len(weights)] <= listtools.weight(result[i])``. ::

      abjad> listtools.partition_by_weights_not_less_than(l, [3], cyclic = True)
      [[0, 1, 2], [3], [4], [5], [6], [7], [8], [9]]

   ::

      abjad> listtools.partition_by_weights_not_less_than(l, [10], cyclic = True)
      [[0, 1, 2, 3, 4], [5, 6], [7, 8]]

   ::

      abjad> listtools.partition_by_weights_not_less_than(l, [3, 10], cyclic = True)
      [[0, 1, 2], [3, 4, 5], [6], [7, 8], [9]]

   When `overhang` is true, allow ``result[-1]`` to have any weight. ::

      abjad> listtools.partition_by_weights_not_less_than(l, [3], overhang = True)
      [[0, 1, 2], [3, 4, 5, 6, 7, 8, 9]]

   ::

      abjad> listtools.partition_by_weights_not_less_than(l, [10], overhang = True)
      [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]

   ::

      abjad> listtools.partition_by_weights_not_less_than(l, [3, 10], overhang = True) 
      [[0, 1, 2], [3, 4, 5], [6, 7, 8, 9]]

   When both `cyclic` and `overhang` are true, 
   partition `l` such that 
   ``weights[i%len(weights)] <= listtools.weight(result[i])``
   and allow ``result[-1]`` to have any weight. ::

      abjad> listtools.partition_by_weights_not_less_than(l, [3], cyclic = True, overhang = True)
      [[0, 1, 2], [3], [4], [5], [6], [7], [8], [9]]

   ::

      abjad> listtools.partition_by_weights_not_less_than(l, [10], cyclic = True, overhang = True)
      [[0, 1, 2, 3, 4], [5, 6], [7, 8], [9]]

   ::

      abjad> listtools.partition_by_weights_not_less_than(l, [3, 10], cyclic = True, overhang = True)
      [[0, 1, 2], [3, 4, 5], [6], [7, 8], [9]]
   '''

   result = [ ]
   l_copy = l[:]
   sublist = [ ]
   cur_weight_index = 0
   i = 0
   while l_copy:
      if cyclic:
         cur_weight = weights[cur_weight_index % len(weights)]
      elif cur_weight_index < len(weights):
         cur_weight = weights[cur_weight_index]
      else:
         break
      n = l_copy.pop(0)
      if not isinstance(n, int):
         raise TypeError('must be integer.')
      sublist.append(n)
      if cur_weight <= listtools_weight(sublist):
         result.append(sublist)
         sublist = [ ]
         cur_weight_index += 1
      i += 1

   if overhang:
      l_copy[0:0] = sublist
      if l_copy:
         result.append(l_copy)

   return result
