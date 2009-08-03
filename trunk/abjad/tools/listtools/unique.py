def unique(l):
   '''Return a newly constructed list of the unique 
   elements in iterable `l`. ::

      abjad> l = [1, 1, 1, 2, 3, 3, 4, 5]
      abjad> listtools.unique(l)
      [1, 2, 3, 4, 5]

   Defined equal to ``list(set(l))``.
   '''

   return list(set(l))
