from abjad.tools import mathtools


def split_sequence_once_by_weights_without_overhang(sequence, weights):
   '''.. versionadded:: 1.1.2

   Split `sequence` once by `weights` without overhang::

      abjad> seqtools.split_sequence_once_by_weights_without_overhang((10, -10, 10, -10), [3, 15, 3])
      [(3,), (7, -8), (-2, 1)]

   Return list of `sequence` types.
   '''

   result = [ ]
   cur_index = 0
   cur_part = [ ]
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
   return result
