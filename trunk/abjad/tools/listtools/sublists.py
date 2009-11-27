from abjad.tools import mathtools


def sublists(l, min_length = None, max_length = None):
   '''.. versionadded:: 1.1.2

   Yield all sublists of list `l` in binary string order. ::

      abjad> list(listtools.sublists([1, 2, 3, 4]))
      [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3], [4], [1, 4], 
      [2, 4], [1, 2, 4], [3, 4], [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]]

   Yield all sublists of list `l` greater than or equal to `min_length`. ::

      abjad> list(listtools.sublists([1, 2, 3, 4], min_length = 3))
      [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]]

   Yield all sublists of list `l` less than or equal to `max_length`. ::

      abjad> list(listtools.sublists([1, 2, 3, 4], max_length = 2))
      [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [4], [1, 4], [2, 4], [3, 4]]

   .. note :: ``listtools.sublists`` will deprecate when Abjad migrates to
      Python 2.6 because Python 2.6 includes built-in subset generation.
   '''

   if not isinstance(l, list):
      raise TypeError('%s must be list.' % l)

   len_l = len(l)
   for i in range(2 ** len_l):
      binary_string = mathtools.binary_string(i)
      binary_string = binary_string.zfill(len_l)
      sublist = [ ]
      for j, digit in enumerate(reversed(binary_string)):
         if digit == '1':
            sublist.append(l[j])
      yield_sublist = True
      if min_length is not None:
         if len(sublist) < min_length:
            yield_sublist = False
      if max_length is not None:
         if max_length < len(sublist):
            yield_sublist = False
      if yield_sublist:
         yield sublist
