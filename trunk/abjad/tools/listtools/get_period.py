from abjad.tools import mathtools
from abjad.tools.listtools.is_uniform import is_uniform
from abjad.tools.listtools.partition_list_cyclically_by_counts_without_overhang import \
   partition_list_cyclically_by_counts_without_overhang


def get_period(iterable):
   '''.. versionadded:: 1.1.2

   Return positive integer period of `iterable`. ::
   
      abjad> listtools.get_period([1, 1, 1, 1, 1, 1])
      1

   ::

      abjad> listtools.get_period([1, 1, 2, 1, 1, 1])
      6

   ::

      abjad> listtools.get_period([1, 1, 2, 1, 1, 2])
      3

   None when `iterable` is empty. ::

      abjad> listtools.get_period([ ]) is None
      True
   '''
   
   iterable = list(iterable)
   if not iterable:
      return None
   for factor in sorted(mathtools.divisors(len(iterable))):
      #print 'factor is %s ...' % factor
      parts = partition_list_cyclically_by_counts_without_overhang(iterable, [factor])
      if is_uniform(parts):
         return factor
   return factor
