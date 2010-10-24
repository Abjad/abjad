def all_are_unequal(l):
   '''.. versionadded:: 1.1.1

   Return ``True`` when the elements in iterable `l` are unique,
   otherwise ``False``. ::

      abjad> l = [1, 1, 1, 2, 3, 3, 4, 5]
      abjad> listtools.all_are_unequal(l)
      False

   Defined equal to ``l == type(l)(set(l))``.

   .. versionchanged:: 1.1.2
      renamed ``listtools.is_unique( )`` to
      ``listtools.all_are_unequal( )``.
   '''

   return l == type(l)(set(l))
