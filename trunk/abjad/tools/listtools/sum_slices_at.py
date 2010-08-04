from abjad.exceptions import InputSpecificationError
from abjad.core import Rational
import types


def sum_slices_at(l, pairs, period = None, overhang = True):
   '''Sum elements in ``l`` according to ``pairs``.
      For each ``(i, count)`` in ``pairs``, 
      replace ``l[i:i+count]`` with ``sum(l[i:i+count])``.

         * When ``period`` is a positive integer, read ``pairs`` cyclically.
         * When ``overhang = False`` do not append incomplete final sum.

      Examples::

         abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
         abjad> listtools.sum_slices_at(l, [(0, 2)], period = 4)
         [1, 2, 3, 9, 6, 7, 17, 10]

         abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
         abjad> listtools.sum_slices_at(l, [(0, 3)], period = 4)
         [6, 3, 15, 7, 27]

         abjad> l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
         abjad> listtools.sum_slices_at(l, [(0, 4)], period = 4)
         [6, 22, 27]

      When ``period`` is not ``None``, indices in ``pairs`` must be less than ``period``.
   '''

   assert isinstance(l, list)
   assert all([isinstance(x, (int, float, Rational)) for x in l])
   assert isinstance(period, (int, types.NoneType))
   assert isinstance(overhang, bool)

   if not _check_sum_slices_at_specification(pairs):
      raise InputSpecificationError('must be list of nonoverlapping pairs.')

   start_indices = set([pair[0] for pair in pairs])
   indices_affected = [ ]
   for pair in pairs:
      indices_affected.extend(range(pair[0], sum(pair)))

   if period is not None:
      if not max(indices_affected) < period:
         raise InputSpecificationError(
            'affected indices must be less than period of repetition.')
   else:
      period = len(l)

   result = [ ]
   slice_remaining = 0
   slice_total = None
   for i, x in enumerate(l):
      if i % period in start_indices:
         index, length = [pair for pair in pairs if pair[0] == i % period][0]
         slice_remaining = length
      if 0 < slice_remaining:
         if slice_total is None:
            slice_total = x
         else:
            slice_total += x
         slice_remaining -= 1

      if slice_remaining == 0:
         if slice_total is not None:
            result.append(slice_total)
            slice_total = None
         else:
            result.append(x)

   if 0 < slice_total:
      if overhang:
         result.append(slice_total)

   return result


def _check_sum_slices_at_specification(pairs):
   try:
      assert isinstance(pairs, list)
      assert all([
         isinstance(x, tuple) and len(x) == 2 and 0 < x[-1]
         for x in pairs])
      indices_affected = [ ]
      for pair in pairs:
         indices_affected.extend(range(pair[0], sum(pair)))
      assert len(indices_affected) == len(set(indices_affected))
   except AssertionError:
     return False
   return True
