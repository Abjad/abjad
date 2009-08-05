from abjad.tools.listtools.flatten import flatten as listtools_flatten
from abjad.tools.listtools.zip_nontruncating import \
   zip_nontruncating as listtools_zip_nontruncating


def interlace(*iterables):
   '''.. versionadded:: 1.1.1

   Interlace elements of arbirarily many `iterables`. ::

      k = range(100, 103)
      l = range(200, 201)
      m = range(300, 303)
      n = range(400, 408)
      t = listtools.interlace(k, l, m, n)
      [100, 200, 300, 400, 101, 301, 401, 102, 302, 402, 403, 404, 405, 406, 407]
   '''

   zipped_iterables = listtools_zip_nontruncating(*iterables)
   flattened_iterables = listtools_flatten(zipped_iterables, depth = 1)

   return flattened_iterables
