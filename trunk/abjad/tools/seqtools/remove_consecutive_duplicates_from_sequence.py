def remove_consecutive_duplicates_from_sequence(sequence):
   '''.. versionadded:: 1.1.2

   Remove consecutive duplciates from `sequence`::

      abjad> list(seqtools.remove_consecutive_duplicates_from_sequence([0, 0, 1, 2, 3, 3, 3, 4, 5]))
      [0, 1, 2, 3, 4, 5]

   Return generator.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.remove_repetitions( )`` to
      ``seqtools.remove_consecutive_duplicates_from_sequence( )``.
   '''

   first_element = False
   for element in sequence:
      if not first_element:
         first_element = True
         yield element
      else:
         if not element == prev_element:
            yield element
      prev_element = element
