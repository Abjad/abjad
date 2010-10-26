def remove_consecutive_duplicates_from_sequence(iterable):
   '''.. versionadded:: 1.1.2

   Yield elements in `iterable` with consecutive
   like elements removed. ::

      abjad> list(listtools.remove_consecutive_duplicates_from_sequence([0, 0, 1, 2, 3, 3, 3, 4, 5]))
      [0, 1, 2, 3, 4, 5]

   .. versionchanged:: 1.1.2
      renamed ``listtools.remove_repetitions( )`` to
      ``listtools.remove_consecutive_duplicates_from_sequence( )``.

   .. versionchanged:: 1.1.2
      renamed ``listtools.remove_consecutive_duplicates_from_iterable( )`` to
      ``listtools.remove_consecutive_duplicates_from_sequence( )``.
   '''

   first_element = False
   for element in iterable:
      if not first_element:
         first_element = True
         yield element
      else:
         if not element == prev_element:
            yield element
      prev_element = element
