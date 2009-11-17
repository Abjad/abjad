from abjad.tools.listtools.all_restricted_growth_functions_of_length import \
   all_restricted_growth_functions_of_length
from abjad.tools.listtools.partition_by_restricted_growth_function import \
   partition_by_restricted_growth_function


def all_set_partitions(l):
   '''.. versionadded:: 1.1.2

   Yield all set partitions of `l` in restricted growth function order. ::

      abjad> for x in listtools.all_set_partitions([21, 22, 23, 24]):
      ...     x
      ... 
      [[21, 22, 23, 24]]
      [[21, 22, 23], [24]]
      [[21, 22, 24], [23]]
      [[21, 22], [23, 24]]
      [[21, 22], [23], [24]]
      [[21, 23, 24], [22]]
      [[21, 23], [22, 24]]
      [[21, 23], [22], [24]]
      [[21, 24], [22, 23]]
      [[21], [22, 23, 24]]
      [[21], [22, 23], [24]]
      [[21, 24], [22], [23]]
      [[21], [22, 24], [23]]
      [[21], [22], [23, 24]]
      [[21], [22], [23], [24]]
   '''

   for rgf in all_restricted_growth_functions_of_length(len(l)):
      partition = partition_by_restricted_growth_function(l, rgf)
      yield partition
