import itertools


def repeat_n_cycles(iterable, n):
   '''.. versionadded:: 1.1.2

   Repeat elements in `iterable` `n` times. ::

      abjad> list(listtools.repeat_n_cycles([1, 2, 3, 4, 5], 3))
      [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]

   Yield nothing when `n` is zero. ::

      abjad> list(listtools.repeat_n_cycles([1, 2, 3, 4, 5], 0))
      [ ]
   '''

   ## TODO: optimize with itertools.from_iterable( ) in Python 2.6 ##

   if n < 0:
      raise ValueError('must be nonnegative.')

   manifest_iterable = list(iterable)
   for x in itertools.chain(*itertools.repeat(manifest_iterable, n)):
      yield x
