import itertools


def repeat_n_cycles(iterable, n):
   '''.. versionadded:: 1.1.2

   Repeat elements in `iterable` `n` times. ::

      abjad> list(listtools.repeat_n_cycles([1, 2, 3, 4, 5], 3))
      [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
   '''

   ## TODO: optimize with itertools.from_iterable( ) in Python 2.6 ##

   if n < 1:
      raise ValueError('must be no less than 1.')

   manifest_iterable = list(iterable)
   for x in itertools.chain(*itertools.repeat(manifest_iterable, n)):
      yield x
