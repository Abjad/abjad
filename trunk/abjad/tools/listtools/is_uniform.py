def is_uniform(iterable):
   '''.. versionadded:: 1.1.2

   True when elements in `iterable` are all the same. ::

      abjad> listtools.is_uniform([99, 99, 99, 99, 99, 99])
      True

   Otherwise false. ::

      abjad> listtools.is_uniform([99, 99, 99, 99, 99, 100])
      False
   '''

   first_element = None
   for element in iterable:
      if first_element is None:
         first_element = element
      else:
         if not element == first_element:
            return False
   return True
