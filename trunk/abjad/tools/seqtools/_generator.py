def _generator(*args):
   '''.. versionadded:: 1.1.2

   Easy-to-instantiate generator version of built-in range(n).

   Intended for use in testing generator input to other seqtools functions.
   '''

   for x in range(*args):
      yield x
