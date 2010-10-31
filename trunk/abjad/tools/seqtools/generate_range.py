def generate_range(*args):
   '''.. versionadded:: 1.1.2

   Generate range::

      abjad> list(seqtools.generate_range(1, 8))
      [1, 2, 3, 4, 5, 6, 7]

   Return generator of nonnegative integers.

   Easy-to-instantiate generator version of built-in range.
   '''

   for x in range(*args):
      yield x
