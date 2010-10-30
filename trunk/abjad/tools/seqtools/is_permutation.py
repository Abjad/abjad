def is_permutation(expr, length = None):
   '''.. versionadded:: 1.1.2

   True when `expr` is a permutation::

      abjad> seqtools.is_permutation([4, 5, 0, 3, 2, 1])
      True

   Otherwise false::

      abjad> seqtools.is_permutation([1, 1, 5, 3, 2, 1])
      False

   True when `expr` is a permutation of `length`::

      abjad> seqtools.is_permutation([4, 5, 0, 3, 2, 1], length = 6)
      True

   Otherwise false::

      abjad> seqtools.is_permutation([4, 0, 3, 2, 1], length = 6)
      False

   Return boolean.

   Permutation of `length` is any ordering of the first `length` nonnegative integers.
   '''

   try:
      if length is None:
         length = len(expr)
      return sorted(expr) == range(length)
   except:
      return False
