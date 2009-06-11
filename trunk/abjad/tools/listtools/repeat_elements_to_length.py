def repeat_elements_to_length(l, length):
   '''Repeat each of the elements in *l* a total of *length* times.

   ::

      abjad> l = [1, 1, 2, 3, 5, 5, 6]
      abjad> listtools.repeat_elements_to_length(l, 2)
      [1, 1, 1, 1, 2, 2, 3, 3, 5, 5, 5, 5, 6, 6]

   ::

      abjad> l = [1, -1, 2, -3, 5, -5, 6]
      abjad> listtools.repeat_elements_to_length(l, 2)
      [1, 1, -1, -1, 2, 2, -3, -3, 5, 5, -5, -5, 6, 6]

   Raise :exc:`TypeError` when *l* is not a list::

      abjad> listtools.repeat_elements_to_length('foo')
      TypeError

   .. todo:: Generalize *length* from a scalar value to list of values.
      Read values cyclically.
   '''

   if not isinstance(l, (list)):
      raise TypeError

   result = [ ]

   for x in l:
      result.extend([x] * length)

   return result
