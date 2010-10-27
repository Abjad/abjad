from abjad.exceptions import PartitionError
from fractions import Fraction
from abjad.tools.seqtools.flatten_sequence import flatten_sequence
from abjad.tools.seqtools.partition_sequence_by_weights import partition_sequence_by_weights
from abjad.tools.mathtools.weight import weight


def group_by_weights(l, weights, 
   fill = 'exact', cyclic = False, overhang = False):
   '''Partition ``l`` into list ``result`` of sublists 
   according to ``weights``.

   Behavior of *fill*:

   *  When ``fill = 'exact'``, ``mathtools.weight(result[i])`` must equal \
      ``weights[i]`` exactly. 
   *  When ``fill = 'less'``, allow ``mathtools.weight(result[i])`` to be \
      just less than, or equal to, ``weights[i]``.
   *  When ``fill = 'greater'``, allow ``mathtools.weight(result[i])`` to be \
      just greater than, or equal to, ``weights[i]``.
   *  Defaults to ``'exact'``.

   Behavior of *cyclic*:

   *  When ``cyclic = False``, read *weights* only once.
   *  When ``cyclic = True``, read *weights* cyclically.
   *  Defaults to ``False``.
   
   Behavior of *overhang*:

   *  When ``overhang = False`` and elements of ``l`` remain, \
      do not append as final part.
   *  When ``overhang = True`` and elements of ``l`` remain, \
      do append as final part.
   *  Defaults to ``False``.

   Raise :exc:`~abjad.exceptions.PartitionError` when

   *  When ``fill = 'exact'`` and ``mathtools.weight(result[i])`` \
      can not equal ``weights[i]`` exactly.
   *  When ``fill = 'less'`` and ``mathtools.weight(result[i])`` 
      exceeds ``weights[i]``.

   Examples:

   ::

      abjad> l = [3, 3, 3, 3, 4, 4, 4, 4, 5, 5]

   ::

      abjad> t = seqtools.group_by_weights(l, [3, 9], fill = 'exact', cyclic = False, overhang = False)
      [[3], [3, 3, 3]]

   ::

      abjad> seqtools.group_by_weights(l, [3, 9], fill = 'exact', cyclic = False, overhang = True)
      [[3], [3, 3, 3], [4, 4, 4, 4, 5, 5]]

   ::

      abjad> t = seqtools.group_by_weights(l, [3, 9], fill = 'exact', cyclic = True, overhang = False)
      PartitionError

   ::

      abjad> seqtools.group_by_weights(l, [3, 9], fill = 'exact', cyclic = True, overhang = True)
      PartitionError

   ::

      abjad> seqtools.group_by_weights(l, [3, 9], fill = 'less', cyclic = False, overhang = False)
      t == [[3], [3, 3, 3]]

   ::

      abjad> seqtools.group_by_weights(l, [3, 9], fill = 'less', cyclic = False, overhang = True)
      [[3], [3, 3, 3], [4, 4, 4, 4, 5, 5]]

   ::

      abjad> seqtools.group_by_weights(l, [3, 9], fill = 'less', cyclic = True, overhang = False)
      PartitionError

   ::

      abjad> t = seqtools.group_by_weights(l, [3, 9], fill = 'less', cyclic = True, overhang = True)
      PartitionError

   ::

      abjad> seqtools.group_by_weights(l, [3, 9], fill = 'greater', cyclic = False, overhang = False)
      [[3], [3, 3, 3]]

   ::

      abjad> seqtools.group_by_weights(l, [3, 9], fill = 'greater', cyclic = False, overhang = True)
      [[3], [3, 3, 3], [4, 4, 4, 4, 5, 5]]

   ::

      abjad> seqtools.group_by_weights(l, [3, 9], fill = 'greater', cyclic = True, overhang = False)
      [[3], [3, 3, 3], [4], [4, 4, 4], [5]]

   ::

      abjad> seqtools.group_by_weights(l, [3, 9], fill = 'greater', cyclic = True, overhang = True)
      [[3], [3, 3, 3], [4], [4, 4, 4], [5], [5]]
   '''

   assert isinstance(l, list)
   assert all([isinstance(x, (int, long, float, Fraction)) for x in l])
   assert isinstance(weights, list)
   assert all([isinstance(x, (int, long, float, Fraction)) for x in weights])
   assert all([0 < x for x in weights])
   assert fill in ('exact', 'less', 'greater')
   assert isinstance(cyclic, bool)
   assert isinstance(overhang, bool)

   if fill == 'exact':
      return _group_by_weights_exact(l, weights, cyclic, overhang)
   elif fill == 'less':
      return _group_by_weights_less(l, weights, cyclic, overhang)
   elif fill == 'greater':
      return _group_by_weights_greater(l, weights, cyclic, overhang)
   else:
      raise ValueError("fill must be 'exact', 'less' or 'greater'.")


def _group_by_weights_exact(l, weights, cyclic, overhang):
   candidate = partition_sequence_by_weights(l, weights, cyclic, overhang) 
   flattened_candidate = flatten_sequence(candidate)
   if flattened_candidate == l[:len(flattened_candidate)]:
      return candidate
   else:
      raise PartitionError('can not partition exactly.') 


def _group_by_weights_less(l, weights, cyclic, overhang):
   if not cyclic:
      return _group_by_weights_less_noncyclic(l, weights, overhang)
   else:
      return _group_by_weights_less_cyclic(l, weights, overhang)


def _group_by_weights_greater(l, weights, cyclic, overhang):
   if not cyclic:
      return _group_by_weights_greater_noncyclic(l, weights, overhang)
   else:
      return _group_by_weights_greater_cyclic(l, weights, overhang)
   

def _group_by_weights_less_noncyclic(l, weights, overhang):

   l_copy = l[:]
   result = [ ]
   cur_part = [ ]

   for target_weight in weights:
      while True:
         try:
            x = l_copy.pop(0)
         except IndexError:
            raise PartitionError('too few elements in l.')
         cur_weight = weight(cur_part)
         candidate_weight = cur_weight + weight([x])
         if candidate_weight < target_weight:
            cur_part.append(x)
         elif candidate_weight == target_weight:
            cur_part.append(x)
            result.append(cur_part)
            cur_part = [ ]
            break
         elif target_weight < candidate_weight:
            if cur_part:
               result.append(cur_part)
               cur_part = [ ]
               l_copy.insert(0, x)
               break
            else:
               raise PartitionError('Elements in l too big.')
         else:
            raise ValueError('candidate and target weights must compare.')

   if overhang:
      left_over = cur_part + l_copy
      if left_over:
         result.append(left_over)

   return result


def _group_by_weights_less_cyclic(l, weights, overhang):

   result = [ ]
   cur_part = [ ]
   cur_target_weight_index = 0
   cur_target_weight = weights[cur_target_weight_index]
   l_copy = l[:]

   while l_copy:
      cur_target_weight = weights[cur_target_weight_index % len(weights)]
      x = l_copy.pop(0)
      cur_part_weight = weight(cur_part)  
      candidate_part_weight = cur_part_weight + weight([x])
      if candidate_part_weight < cur_target_weight:
         cur_part.append(x)
      elif candidate_part_weight == cur_target_weight:
         cur_part.append(x)
         result.append(cur_part)
         cur_part = [ ]
         cur_target_weight_index += 1
      elif cur_target_weight < candidate_part_weight:
         if cur_part:
            l_copy.insert(0, x)
            result.append(cur_part)
            cur_part = [ ]
            cur_target_weight_index += 1
         else:
            raise PartitionError('Elements in l too big.')
      else:
         raise ValueError('candidate and target rates must compare.')

   if cur_part:
      if overhang:
         result.append(cur_part)

   return result
   

def _group_by_weights_greater_noncyclic(l, weights, overhang):
   
   result = [ ]
   cur_part = [ ]
   l_copy = l[:]

   for num_weight, target_weight in enumerate(weights):
      while True:
         try:
            x = l_copy.pop(0)
         except IndexError:
            if num_weight + 1 == len(weights):
               if cur_part:
                  result.append(cur_part)
                  break
            raise PartitionError('too few elements in l.')
         cur_part.append(x)
         if target_weight <= weight(cur_part):
            result.append(cur_part)
            cur_part = [ ]
            break
   if l_copy:
      if overhang:
         result.append(l_copy)
   return result 


def _group_by_weights_greater_cyclic(l, weights, overhang):

   l_copy = l[:]
   result = [ ]
   cur_part = [ ]
   target_weight_index = 0
   len_weights = len(weights)

   while l_copy:
      target_weight = weights[target_weight_index % len_weights]
      x = l_copy.pop(0)
      cur_part.append(x)
      if target_weight <= weight(cur_part):
         result.append(cur_part)
         cur_part = [ ]
         target_weight_index += 1

   assert not l_copy

   if cur_part:
      if overhang:
         result.append(cur_part)

   return result
