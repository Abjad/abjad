def is_permutation(expr, length = None):
   '''.. versionadded:: 1.1.2

   True when `expr` is a permutation::

      abjad> from abjad.tools import seqtools

   ::

      abjad> seqtools.is_permutation([4, 5, 0, 3, 2, 1])
      True

   Otherwise false::

      abjad> seqtools.is_permutation([1, 1, 5, 3, 2, 1])
      False

   True when `expr` is a permutation of first `length` nonnegative integers::

      abjad> seqtools.is_permutation([4, 5, 0, 3, 2, 1], length = 6)
      True

   Otherwise false::

      abjad> seqtools.is_permutation([4, 0, 3, 2, 1], length = 6)
      False

   Return boolean.
   '''

   try:
      if length is None:
         length = len(expr)
      return sorted(expr) == range(length)
   except:
      return False
