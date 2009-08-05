def is_unique(l):
   '''.. versionadded:: 1.1.1

   Return ``True`` when the elements in iterable `l` are unique,
   otherwise ``False``. ::

      abjad> l = [1, 1, 1, 2, 3, 3, 4, 5]
      abjad> listtools.is_unique(l)
      False

   Defined equal to ``l == type(l)(set(l))``.
   '''

   return l == type(l)(set(l))
