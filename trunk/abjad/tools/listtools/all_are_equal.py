def all_are_equal(iterable):
   '''.. versionadded:: 1.1.2

   True when elements in `iterable` are all the same. ::

      abjad> listtools.all_are_equal([99, 99, 99, 99, 99, 99])
      True

   Otherwise false. ::

      abjad> listtools.all_are_equal([99, 99, 99, 99, 99, 100])
      False

   .. versionchanged:: 1.1.2
      renamed ``listtools.is_uniform( )`` to
      ``listtools.all_are_equal( )``.
   '''

   first_element = None
   for element in iterable:
      if first_element is None:
         first_element = element
      else:
         if not element == first_element:
            return False
   return True
