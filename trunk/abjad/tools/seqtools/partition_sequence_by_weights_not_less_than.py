#from abjad.tools import mathtools
#from abjad.tools.mathtools.weight import weight
from abjad.tools.seqtools._group_sequence_elements_by_weights_at_least import _group_sequence_elements_by_weights_at_least


def partition_sequence_by_weights_not_less_than(sequence, weights, 
   cyclic = False, overhang = False):
   r'''.. versionadded:: 1.1.2

   Partition `sequence` into sublists ``result[0], ..., result[n]`` such that
   ``weights[i] <= mathtools.weight(result[i])``::

      abjad> seqtools.partition_sequence_by_weights_not_less_than(range(10), [3])
      [[0, 1, 2]]

   ::

      abjad> seqtools.partition_sequence_by_weights_not_less_than(range(10), [10])
      [[0, 1, 2, 3, 4]]

   ::

      abjad> seqtools.partition_sequence_by_weights_not_less_than(range(10), [3, 10])
      [[0, 1, 2], [3, 4, 5]]

   When `cyclic` is true, partition `sequence` such that
   ``weights[i%len(weights)] <= mathtools.weight(result[i])``::

      abjad> seqtools.partition_sequence_by_weights_not_less_than(range(10), [3], cyclic = True)
      [[0, 1, 2], [3], [4], [5], [6], [7], [8], [9]]

   ::

      abjad> seqtools.partition_sequence_by_weights_not_less_than(range(10), [10], cyclic = True)
      [[0, 1, 2, 3, 4], [5, 6], [7, 8]]

   ::

      abjad> seqtools.partition_sequence_by_weights_not_less_than(range(10), [3, 10], cyclic = True)
      [[0, 1, 2], [3, 4, 5], [6], [7, 8], [9]]

   When `overhang` is true, allow ``result[-1]`` to have any weight. ::

      abjad> seqtools.partition_sequence_by_weights_not_less_than(range(10), [3], overhang = True)
      [[0, 1, 2], [3, 4, 5, 6, 7, 8, 9]]

   ::

      abjad> seqtools.partition_sequence_by_weights_not_less_than(range(10), [10], overhang = True)
      [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]

   ::

      abjad> seqtools.partition_sequence_by_weights_not_less_than(range(10), [3, 10], overhang = True) 
      [[0, 1, 2], [3, 4, 5], [6, 7, 8, 9]]

   When both `cyclic` and `overhang` are true, partition `sequence` such that 
   ``weights[i%len(weights)] <= mathtools.weight(result[i])``
   and allow ``result[-1]`` to have any weight::

      abjad> seqtools.partition_sequence_by_weights_not_less_than(range(10), [3], cyclic = True, overhang = True)
      [[0, 1, 2], [3], [4], [5], [6], [7], [8], [9]]

   ::

      abjad> seqtools.partition_sequence_by_weights_not_less_than(range(10), [10], cyclic = True, overhang = True)
      [[0, 1, 2, 3, 4], [5, 6], [7, 8], [9]]

   ::

      abjad> seqtools.partition_sequence_by_weights_not_less_than(range(10), [3, 10], cyclic = True, overhang = True)
      [[0, 1, 2], [3, 4, 5], [6], [7, 8], [9]]

   .. versionchanged:: 1.1.2
      renamed ``seqtools.partition_sequence_by_weights_not_less_than( )`` to
      ``seqtools.partition_sequence_by_weights_not_less_than( )``.
   '''

   return _group_sequence_elements_by_weights_at_least(sequence, weights, cyclic = cyclic, overhang = overhang)

#   result = [ ]
#   sequence_copy = sequence[:]
#   sublist = [ ]
#   cur_weight_index = 0
#   i = 0
#   while sequence_copy:
#      if cyclic:
#         cur_weight = weights[cur_weight_index % len(weights)]
#      elif cur_weight_index < len(weights):
#         cur_weight = weights[cur_weight_index]
#      else:
#         break
#      n = sequence_copy.pop(0)
#      if not isinstance(n, int):
#         raise TypeError('must be integer.')
#      sublist.append(n)
#      if cur_weight <= weight(sublist):
#         result.append(sublist)
#         sublist = [ ]
#         cur_weight_index += 1
#      i += 1
#
#   if overhang:
#      sequence_copy[0:0] = sublist
#      if sequence_copy:
#         result.append(sequence_copy)
#
#   return result
