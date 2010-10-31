from abjad.tools import mathtools
from abjad.tools.seqtools.repeat_sequence_to_weight import repeat_sequence_to_weight


def _split_sequence_by_weights(sequence, weights, cyclic = False, overhang = False):
   '''.. versionadded:: 1.1.2

   Split sequence by weights.

   Return list of sequence types.
   '''

   result = [ ]
   cur_index = 0
   cur_part = [ ]
   if cyclic:
      weights = repeat_sequence_to_weight(
         weights, mathtools.weight(sequence), remainder = 'less')
   for weight in weights:
      cur_part_weight = mathtools.weight(cur_part)
      while cur_part_weight < weight:
         cur_part.append(sequence[cur_index])
         cur_index += 1
         cur_part_weight = mathtools.weight(cur_part)
      if cur_part_weight == weight:
         cur_part = type(sequence)(cur_part)
         result.append(cur_part)
         cur_part = [ ]
      elif weight < cur_part_weight:
         overage = cur_part_weight - weight
         cur_last_element = cur_part.pop(-1)
         needed = abs(cur_last_element) - overage
         needed *= mathtools.sign(cur_last_element)
         cur_part.append(needed)
         cur_part = type(sequence)(cur_part)
         result.append(cur_part)
         overage *= mathtools.sign(cur_last_element)
         cur_part = [overage]
   
   if overhang:
      last_part = cur_part
      last_part.extend(sequence[cur_index:])
      last_part = type(sequence)(last_part)
      result.append(last_part)

   return result
