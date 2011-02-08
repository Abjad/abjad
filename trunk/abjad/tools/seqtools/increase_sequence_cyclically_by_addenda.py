def increase_sequence_cyclically_by_addenda(sequence, addenda, shield = True, trim = True):
   '''Increase `sequence` cyclically by `addenda`::

      abjad> sequence = range(10)
      abjad> seqtools.increase_sequence_cyclically_by_addenda(sequence, [2, 0])
      [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]

   ::

      abjad> sequence = range(10)
      abjad> seqtools.increase_sequence_cyclically_by_addenda(sequence, [10, -10])
      [10, 1, 12, 1, 14, 1, 16, 1, 18, 1]

   ::

      abjad> sequence = range(10)
      abjad> seqtools.increase_sequence_cyclically_by_addenda(sequence, [10, -10], shield = False)
      [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]

   Map nonpositive values to ``1`` by default.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.increase_cyclic( )`` to
      ``seqtools.increase_sequence_cyclically_by_addenda( )``.
   '''

   if not isinstance(sequence, (list, tuple)):
      raise TypeError

   result = [ ]

   for i, element in enumerate(sequence):
      new = element + addenda[i % len(addenda)]
      if shield and new <= 0:
         new = 1
      result.append(new)

   return result
