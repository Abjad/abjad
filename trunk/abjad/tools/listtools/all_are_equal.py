def all_are_equal(sequence):
   '''.. versionadded:: 1.1.2

   True when all elements in `sequence` are equal::

      abjad> listtools.all_are_equal([99, 99, 99, 99, 99, 99])
      True

   True on empty `sequence`::

      abjad> listtools.all_are_equal([ ])
      True

   False otherwise::

      abjad> listtools.all_are_equal([99, 99, 99, 99, 99, 100])
      False

   Return boolean.

   .. versionchanged:: 1.1.2
      renamed ``listtools.is_uniform( )`` to
      ``listtools.all_are_equal( )``.
   '''

   first_element = None
   for element in sequence:
      if first_element is None:
         first_element = element
      else:
         if not element == first_element:
            return False
   return True
