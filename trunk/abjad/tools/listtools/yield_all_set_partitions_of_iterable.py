from abjad.tools.listtools.generate_all_restricted_growth_functions_of_length import \
   generate_all_restricted_growth_functions_of_length
from abjad.tools.listtools.partition_by_restricted_growth_function import \
   partition_by_restricted_growth_function


def yield_all_set_partitions_of_iterable(l):
   '''.. versionadded:: 1.1.2

   Yield all set partitions of `l` in restricted growth function order. ::

      abjad> for x in listtools.yield_all_set_partitions_of_iterable([21, 22, 23, 24]):
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

   .. versionchanged:: 1.1.2
      renamed ``listtools.all_set_partitions( )`` to
      ``listtools.yield_all_set_partitions_of_iterable( )``.
   '''

   for rgf in generate_all_restricted_growth_functions_of_length(len(l)):
      partition = partition_by_restricted_growth_function(l, rgf)
      yield partition
