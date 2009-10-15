from abjad.tools import mathtools


def sublists(l):
   '''.. versionadded:: 1.1.2

   Yield all sublists of list `l` in binary string order. ::

      abjad> list(listtools.sublists([1, 2, 3, 4]))
      [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3], [4], [1, 4], 
      [2, 4], [1, 2, 4], [3, 4], [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]]

   ::

      abjad> list(listtools.sublists(list('text')))
      [[], ['t'], ['e'], ['t', 'e'], ['x'], ['t', 'x'], ['e', 'x'], 
      ['t', 'e', 'x'], ['t'], ['t', 't'], ['e', 't'], ['t', 'e', 't'], 
      ['x', 't'], ['t', 'x', 't'], ['e', 'x', 't'], ['t', 'e', 'x', 't']]

   .. note :: ``listtools.sublists`` will deprecate when Abjad migrates to
      Python 2.6 because Python 2.6 includes built-in subset generation.
   '''

   if not isinstance(l, list):
      raise TypeError('%s must be list.' % l)

   sublists = [ ]

   len_l = len(l)
   for i in range(2 ** len_l):
      binary_string = mathtools.binary_string(i)
      binary_string = binary_string.zfill(len_l)
      subset = [ ]
      for j, digit in enumerate(reversed(binary_string)):
         if digit == '1':
            subset.append(l[j])
      yield subset
