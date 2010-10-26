import itertools


def repeat_sequence_n_times(iterable, n):
   '''.. versionadded:: 1.1.2

   Repeat elements in `iterable` `n` times. ::

      abjad> list(listtools.repeat_sequence_n_times([1, 2, 3, 4, 5], 3))
      [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]

   Yield nothing when `n` is zero. ::

      abjad> list(listtools.repeat_sequence_n_times([1, 2, 3, 4, 5], 0))
      [ ]

   .. versionchanged:: 1.1.2
      renamed ``listtools.repeat_n_cycles( )`` to
      ``listtools.repeat_sequence_n_times( )``.

   .. versionchanged:: 1.1.2
      renamed ``listtools.repeat_iterable_n_times( )`` to
      ``listtools.repeat_sequence_n_times( )``.
   '''

   ## TODO: optimize with itertools.from_iterable( ) in Python 2.6 ##

   if n < 0:
      raise ValueError('must be nonnegative.')

   manifest_iterable = list(iterable)
   for x in itertools.chain(*itertools.repeat(manifest_iterable, n)):
      yield x
