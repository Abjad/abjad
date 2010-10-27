from abjad.tools.listtools.flatten_sequence import flatten_sequence
from abjad.tools.listtools.zip_sequences_nontruncating import zip_sequences_nontruncating


def interlace_sequences(*iterables):
   '''.. versionadded:: 1.1.1

   Interlace elements of arbirarily many `iterables`. ::

      k = range(100, 103)
      l = range(200, 201)
      m = range(300, 303)
      n = range(400, 408)
      t = listtools.interlace_sequences(k, l, m, n)
      [100, 200, 300, 400, 101, 301, 401, 102, 302, 402, 403, 404, 405, 406, 407]

   .. versionchanged:: 1.1.2
      renamed ``listtools.interlace( )`` to
      ``listtools.interlace_sequences( )``.

   .. versionchanged:: 1.1.2
      renamed ``listtools.interlace_iterables( )`` to
      ``listtools.interlace_sequences( )``.
   '''

   zipped_iterables = zip_sequences_nontruncating(*iterables)
   flattened_iterables = flatten_sequence(zipped_iterables, depth = 1)

   return flattened_iterables
