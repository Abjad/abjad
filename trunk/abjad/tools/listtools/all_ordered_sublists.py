from abjad.tools import mathtools


def all_ordered_sublists(l):
   '''.. versionadded:: 1.1.2

   Yield all ordered sublists of list `l`. ::

      abjad> for x in listtools.all_ordered_sublists(l):
      ...     x
      ... 
      [[0, 1, 2, 3]]
      [[0, 1, 2], [3]]
      [[0, 1], [2, 3]]
      [[0, 1], [2], [3]]
      [[0], [1, 2, 3]]
      [[0], [1, 2], [3]]
      [[0], [1], [2, 3]]
      [[0], [1], [2], [3]]


   .. todo:: write tests.
   '''

   if not isinstance(l, list):
      raise TypeError('%s must be list.' % l)

   partitions = [ ]

   len_l_minus_1 = len(l) - 1
   for i in range(2 ** len_l_minus_1):
      binary_string = mathtools.binary_string(i)
      binary_string = binary_string.zfill(len_l_minus_1)
      part = l[0:1]
      partition = [part]
      for n, indicator in zip(l[1:], binary_string):
         if int(indicator) == 0:
            part.append(n)
         else:
            part = [n]
            partition.append(part)
      partitions.append(partition)

   return partitions
      
