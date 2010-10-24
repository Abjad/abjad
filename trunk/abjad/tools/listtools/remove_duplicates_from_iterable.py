def remove_duplicates_from_iterable(l):
   '''Return a newly constructed list of the unique 
   elements in iterable `l`. ::

      abjad> l = [1, 1, 1, 2, 3, 3, 4, 5]
      abjad> listtools.remove_duplicates_from_iterable(l)
      [1, 2, 3, 4, 5]

   Defined equal to ``list(set(l))``.

   .. versionchanged:: 1.1.2
      renamed ``listtools.unique( )`` to
      ``listtools.remove_duplicates_from_iterable( )``.
   '''

   return list(set(l))
