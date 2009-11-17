from abjad.tools.listtools.is_restricted_growth_function import \
   is_restricted_growth_function


def partition_by_restricted_growth_function(l, restricted_growth_function):
   '''.. versionadded:: 1.1.2

   Partition `l` by `restricted_growth_function`. ::

      abjad> l = range(10)
      abjad> rgf = [1, 1, 2, 2, 1, 2, 3, 3, 2, 4]
      abjad> listtools.partition_by_restricted_growth_function(l, rgf)
      [[0, 1, 4], [2, 3, 5, 8], [6, 7], [9]]

   Raise exception when ``len(l)`` does not equal 
   ``len(restricted_growth_function)``. ::

      abjad> l = range(10)
      abjad> rgf = [1, 1, 2]
      abjad> listtools.partition_by_restricted_growth_function(l, rgf)
      ValueError
   '''

   if not is_restricted_growth_function(restricted_growth_function):
      raise ValueError('must be restricted growth function.')

   if not len(l) == len(restricted_growth_function):
      raise ValueError('lengths must be equal.')
   
   partition = [ ]
   for part_index in range(max(restricted_growth_function)):
      part = [ ]
      partition.append(part)

   for n, part_number in zip(l, restricted_growth_function):
      part_index = part_number - 1
      part = partition[part_index] 
      part.append(n)

   return partition
