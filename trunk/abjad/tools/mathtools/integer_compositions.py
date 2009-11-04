from abjad.tools.mathtools.integer_partitions import integer_partitions \
   as mathtools_integer_partitions


def integer_compositions(n):
   r'''.. versionadded:: 1.1.2

   Yield all compositions (that is, **ordered** partitions) of 
   positive integer `n` in descending lex order. ::

      abjad> for integer_composition in mathtools.integer_compositions(5):
      ...     integer_composition
      ... 
      (5,)
      (4, 1)
      (3, 2)
      (3, 1, 1)
      (2, 3)
      (2, 2, 1)
      (2, 1, 2)
      (2, 1, 1, 1)
      (1, 4)
      (1, 3, 1)
      (1, 2, 2)
      (1, 2, 1, 1)
      (1, 1, 3)
      (1, 1, 2, 1)
      (1, 1, 1, 2)
      (1, 1, 1, 1, 1)
   '''

   from abjad.tools.listtools.permutations import permutations as \
      listtools_permutations

   ## definitely not optimized
   ## ... though shouldn't matter unless 
   ## generating MANY compositions 

   compositions = set([ ])
   for partition in mathtools_integer_partitions(n):
      for permutation in listtools_permutations(partition):
         compositions.add(permutation)
   for composition in reversed(sorted(compositions)):
      yield composition
