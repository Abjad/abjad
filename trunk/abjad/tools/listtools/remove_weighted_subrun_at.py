from abjad.core import Rational


def remove_weighted_subrun_at(l, weight, i):
   '''Remove weighted subrun of weight ``weight`` from ``l`` at index ``i``.

   Examples::

      abjad> l = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
      abjad> listtools.remove_weighted_subrun_at(l, 8, 0)
      [4, 5, 1, 2, 5, 5, 6]

      abjad> l = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
      abjad> listtools.remove_weighted_subrun_at(l, 13, 4)
      [1, 1, 2, 3, 5, 5, 6]
   '''

   result = l[:i]
   total = 0

   for element in l[i:]:
      if weight <= total:
         result.append(element)
      elif weight < total + element:
         result.append(total + element - weight)
      total += element

   return result
