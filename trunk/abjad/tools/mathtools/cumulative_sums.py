def cumulative_sums(sequence):
   '''Cumulative sums of `sequence`::

      abjad> mathtools.cumulative_sums([1, 2, 3, 4, 5, 6, 7, 8])
      [1, 3, 6, 10, 15, 21, 28, 36]

   Raise type error when `sequence` is neither list nor tuple::

      abjad> mathtools.cumulative_sums('foo')
      TypeError

   Raise value error on empty `sequence`::

      abjad> mathtools.cumulative_sums([ ])
      ValueError

   Return list.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.cumulative_sums( )`` to
      ``mathtools.cumulative_sums( )``.
   '''


   if not isinstance(sequence, (list, tuple)):
      raise TypeError

   if len(sequence) == 0:
      raise ValueError

   result = [sequence[0]]
   for element in sequence[1:]:
      result.append(result[-1] + element) 

   return result
