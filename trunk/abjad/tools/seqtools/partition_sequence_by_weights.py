from abjad.tools import mathtools
from abjad.tools.mathtools.weight import weight
from fractions import Fraction


def partition_sequence_by_weights(sequence, weights, cyclic = False, overhang = False):
   '''Partition `sequence` by `weights`.
   

   With one-element ``weights``::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [15])
      [[15]]

   ::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [15], cyclic = True)
      [[15], [5, 10], [10, 5], [15], [15]]

   ::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [15], overhang = True)
      [[15], [5, 20, 20, 20]]

   ::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [15], cyclic = True, overhang = True)
      [[15], [5, 10], [10, 5], [15], [15], [5]]

   With multi-element ``weights``::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [7, 15])
      [[7], [13, 2]]

   ::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [7, 15], cyclic = True)
      [[7], [13, 2], [7], [11, 4], [9, 6], [7]]

   ::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [7, 15], overhang = True)
      [[7], [13, 2], [18, 20, 20]]

   ::

      abjad> seqtools.partition_sequence_by_weights([20, 20, 20, 20], [7, 15], cyclic = True, overhang = True)
      [[7], [13, 2], [7], [11, 4], [7], [9, 6], [7], [7]]

   Because ``mathtools.weight(sequence)`` equals the sum of the absolute
   values of the elements in list `sequence`, negative numbers in `sequence`
   give negative numbers in the output of ``seqtools.partition_sequence_by_weights( )``::

      abjad> seqtools.partition_sequence_by_weights([20, -20, 20, -20], [7, 15], cyclic = True)
      [[7], [13, -2], [-7], [-11, 4], [7], [9, -6], [-7]]

   Set `weights` to any iterable of one or more positive numbers.

   Set `cyclic` to true or false.

   Set `overhang` to true or false.

   Return ``result`` comprising sublists such that ``mathtools.weight(r_i)`` 
   for ``r_i`` in ``result`` equals ``s_i`` for ``s_i`` in list of weights ``s``.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.partition_by_weights( )`` to
      ``seqtools.partition_sequence_by_weights( )``.
   '''

   assert all([isinstance(x, (int, float, long, Fraction)) for x in sequence])
   assert all([isinstance(x, (int, float, long, Fraction)) for x in weights])
   assert all([0 < x for x in weights])

   copy_of_sequence = sequence[:]
   result = [[ ]]
   cur_target_weight_index = 0
   cur_target_weight = weights[cur_target_weight_index] 

   while copy_of_sequence:
      cur_part = result[-1]
      cur_weight = weight(cur_part)
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
                  result.append(copy_of_sequence)
               return result
      elif cur_weight < cur_target_weight:
         if copy_of_sequence:
            x = copy_of_sequence.pop(0)
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
               copy_of_sequence.insert(0, right_addend)
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
