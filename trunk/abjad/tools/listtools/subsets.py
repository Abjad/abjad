from abjad.tools import mathtools


def subsets(l):
   '''Yield all subsets of list `l` in binary string order.

   ::

      abjad> list(listtools.subsets([1, 2, 3, 4]))
      [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3], [4], [1, 4], 
      [2, 4], [1, 2, 4], [3, 4], [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]]

   ::

      abjad> list(listtools.subsets(list('text')))
      [[], ['t'], ['e'], ['t', 'e'], ['x'], ['t', 'x'], ['e', 'x'], 
      ['t', 'e', 'x'], ['t'], ['t', 't'], ['e', 't'], ['t', 'e', 't'], 
      ['x', 't'], ['t', 'x', 't'], ['e', 'x', 't'], ['t', 'e', 'x', 't']]

   .. note :: ``listtools.subsets`` will deprecate when Abjad migrates to
      Python 2.6 because Python 2.6 includes built-in subset generation.
   '''

   if not isinstance(l, list):
      raise TypeError('%s must be list.' % l)

   subsets = [ ]

   len_l = len(l)
   for i in range(2 ** len_l):
      binary_string = mathtools.binary_string(i)
      binary_string = binary_string.zfill(len_l)
      subset = [ ]
      for j, digit in enumerate(reversed(binary_string)):
         if digit == '1':
            subset.append(l[j])
      yield subset
