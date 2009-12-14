from abjad.tools.listtools.pairwise import pairwise


def count_repetitions(iterable):
   '''.. versionadded:: 1.1.2

   Return nonnegative integer number of two-element repetitions 
   in `iterable`. ::

      abjad> listtools.count_repetitions([0, 0, 1, 1, 1, 2, 3, 4, 5])
      3
   '''

   total_repetitions = 0
   for left, right in pairwise(iterable):
      if left == right:
         total_repetitions += 1

   return total_repetitions
