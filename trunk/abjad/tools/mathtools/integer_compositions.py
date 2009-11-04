from abjad.tools.mathtools.binary_string import binary_string as \
   mathtools_binary_string
import itertools


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

   ## Finds small values of n easily.
   ## Takes ca. 4 seconds for n = 17.

   compositions = [ ]

   x = 0
   string_length = n
   while x < 2 ** (n - 1):
      string = mathtools_binary_string(x)
      string = string.zfill(string_length)
      l = [int(c) for c in list(string)]
      partition = [ ]
      g = itertools.groupby(l, lambda x: x)
      for value, group in g:
         partition.append(list(group))
      sublengths = [len(part) for part in partition]
      composition = tuple(sublengths)
      compositions.append(composition)
      x += 1

   for composition in reversed(sorted(compositions)):
      yield composition
