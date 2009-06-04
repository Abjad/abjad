from abjad.rational.rational import Rational
from abjad.tools import mathtools
from abjad.tools.listtools.flatten import flatten as listtools_flatten
from abjad.tools.listtools.weight import weight as listtools_weight


def partition_by_weights(l, weights, cyclic = False, overhang = False):
   '''Partition list ``l`` into ``result`` comprising sublists \
   such that ``listtools.weight(r_i)`` for ``r_i`` in ``result`` equals \
   ``s_i`` for ``s_i`` in list of weights ``s``.

   Input:

   * ``l``: any iterable comprising positive, negative or zero-valued numbers.
   * ``weights``: any iterable of one or more positive numbers.

   Ouput: Python list of one or more sublists.

   With one-element ``weights`` list.

   ::

      abjad> l = [20, 20, 20, 20] 
      abjad> listtools.partition_by_weights(l, [15])
      [[15]]

   ::

      abjad> l = [20, 20, 20, 20] 
      abjad> listtools.partition_by_weights(l, [15], cyclic = True)
      [[15], [5, 10], [10, 5], [15], [15]]

   ::

      abjad> l = [20, 20, 20, 20] 
      abjad> listtools.partition_by_weights(l, [15], overhang = True)
      [[15], [5, 20, 20, 20]]

   ::

      abjad> l = [20, 20, 20, 20]
      abjad> listtools.partition_by_weights(l, [15], cyclic = True, overhang = True)
      [[15], [5, 10], [10, 5], [15], [15], [5]]

   With multi-element ``weights`` list.

   ::

      abjad> l = [20, 20, 20, 20]
      abjad> listtools.partition_by_weights(l, [7, 15])
      [[7], [13, 2]]

   ::

      abjad> l = [20, 20, 20, 20]
      abjad> listtools.partition_by_weights(l, [7, 15], cyclic = True)
      [[7], [13, 2], [7], [11, 4], [9, 6], [7]]

   ::

      abjad> l = [20, 20, 20, 20]
      abjad> listtools.partition_by_weights(l, [7, 15], overhang = True)
      [[7], [13, 2], [18, 20, 20]]

   ::

      abjad> l = [20, 20, 20, 20]
      abjad> listtools.partition_by_weights(l, [7, 15], cyclic = True, overhang = True)
      [[7], [13, 2], [7], [11, 4], [7], [9, 6], [7], [7]]

   Because ``listtools.weight(l)`` equals the sum of the absolute \
   values of the elements in list ``l``, negative numbers in ``l`` \
   give negative numbers in the output of \
   ``listtools.partition_by_weights( )``.

   ::

      abjad> l = [20, -20, 20, -20]
      abjad> listtools.partition_by_weights(l, [7, 15], cyclic = True)
      [[7], [13, -2], [-7], [-11, 4], [7], [9, -6], [-7]]'''

   assert all([isinstance(x, (int, float, long, Rational)) for x in l])
   assert all([isinstance(x, (int, float, long, Rational)) for x in weights])
   assert all([0 < x for x in weights])

   copy_of_l = l[:]
   result = [[ ]]
   cur_target_weight_index = 0
   cur_target_weight = weights[cur_target_weight_index] 

   while copy_of_l:
      cur_part = result[-1]
      cur_weight = listtools_weight(cur_part)
      if cur_weight == cur_target_weight:
         cur_target_weight_index += 1
         if cyclic:
            cyclic_weight_index = cur_target_weight_index % len(weights)
            cur_target_weight = weights[cyclic_weight_index]
            result.append([ ])
         else:
            if len(result) < len(weights):
               cur_target_weight = weights[cur_target_weight_index]
               result.append([ ])
            else:
               if cur_part == [ ]:
                  result.pop( )
               if overhang:
                  result.append(copy_of_l)
               return result
      elif cur_weight < cur_target_weight:
         if copy_of_l:
            x = copy_of_l.pop(0)
            candidate_weight = cur_weight + abs(x)
            if candidate_weight <= cur_target_weight:
               cur_part.append(x)
            else:
               sign_of_x = mathtools.sign(x)
               left_addend = cur_target_weight - cur_weight
               right_addend = abs(x) - left_addend
               left_addend *= sign_of_x
               right_addend *= sign_of_x
               cur_part.append(left_addend)
               copy_of_l.insert(0, right_addend)
         else:
            if cur_part == [ ]:
               result.pop( )
            return result
      else:
         raise ValueError('cur_weight should be <= cur_target_weight.')

   if cur_weight < cur_target_weight:
      if not overhang:
         result.pop( )

   return result
