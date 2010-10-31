def get_indices_of_sequence_elements_equal_to_true(l):
   '''Return the nonnegative integers ``i, j, ...``
   for which ``l[i], l[j], ...`` are ``True``.

   ::

      abjad> l = [0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1]
      abjad> seqtools.get_indices_of_sequence_elements_equal_to_true(l)
      [3, 4, 5, 9, 10, 11]

   ::

      abjad> l = [0, 0, 0, 0, 0, 0]
      abjad> seqtools.get_indices_of_sequence_elements_equal_to_true(l)
      [ ]

   Raise :exc:`TypeError` when *l* is neither list nor tuple::

      abjad> seqtools.get_indices_of_sequence_elements_equal_to_true('foo')
      TypeError

   .. versionchanged:: 1.1.2
      renamed ``seqtools.true_indices( )`` to
      ``seqtools.get_indices_of_sequence_elements_equal_to_true( )``.
   '''

   if not isinstance(l, (list, tuple)):
      raise TypeError

   result = [ ]

   for i, x in enumerate(l):
      if bool(x):
         result.append(i)

   return result
