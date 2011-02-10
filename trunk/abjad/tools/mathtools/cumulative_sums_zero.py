def cumulative_sums_zero(sequence):
   '''Cumulative sums of `sequence` starting from ``0``::

      abjad> mathtools.cumulative_sums_zero([1, 2, 3, 4, 5, 6, 7, 8])
      [0, 1, 3, 6, 10, 15, 21, 28, 36]

   Raise value error on empty `sequence`::

      abjad> mathtools.cumulative_sums_zero([ ])
      ValueError

   Return list.

   .. versionchanged:: 1.1.2
      renamed ``mathtools.cumulative_sums_zero( )`` to
      ``mathtools.cumulative_sums_zero( )``.
   '''

   result = [0]
   for element in sequence:
      result.append(result[-1] + element) 

   return result
