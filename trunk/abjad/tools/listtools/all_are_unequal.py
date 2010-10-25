def all_are_unequal(sequence):
   '''.. versionadded:: 1.1.1

   True when all elements in `sequence` are unequal::

      abjad> listtools.all_are_unequal([1, 2, 3, 4, 9])
      True

   True on empty `sequence`::

      abjad> listtools.all_are_unequal([ ])
      True

   False otherwise::

      abjad> listtools.all_are_unequal([1, 2, 3, 4, 4])
      False

   Return boolean.

   .. versionchanged:: 1.1.2
      renamed ``listtools.is_unique( )`` to
      ``listtools.all_are_unequal( )``.
   '''

   return sequence == type(sequence)(set(sequence))
