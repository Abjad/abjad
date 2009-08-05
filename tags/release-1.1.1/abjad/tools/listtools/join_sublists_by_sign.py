from abjad.tools.listtools.sign import sign as listtools_sign


def join_sublists_by_sign(l):
   '''Join sublists in list *l* by sign.

   ::

      abjad> l = [[1, 2], [3, 4], [-5, -6, -7], [-8, -9, -10], [11, 12]]
      abjad> t = listtools.join_sublists_by_sign(l)
      [[1, 2, 3, 4], [-5, -6, -7, -8, -9, -10], [11, 12]]

   ::

      abjad> l = [[1, 2], [], [], [3, 4, 5], [6, 7]]
      abjad> t = listtools.join_sublists_by_sign(l)
      [[1, 2], [], [3, 4, 5, 6, 7]]
   '''

   if not isinstance(l, list):
      raise TypeError

   if not all([isinstance(x, list) for x in l]):
      raise TypeError

   if any([listtools_sign(x) is None for x in l]):
      raise ValueError

   result = [ ]

   for sublist in l:
      try:
         prev_sublist = result[-1]
         if listtools_sign(prev_sublist) == listtools_sign(sublist):
            prev_sublist.extend(sublist)
         else:
            result.append(sublist[:])
      except IndexError:
         result.append(sublist[:])

   return result
