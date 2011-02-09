def remove_consecutive_duplicates_from_sequence(sequence):
   '''.. versionadded:: 1.1.2

   Remove consecutive duplicates from `sequence`::

      abjad> seqtools.remove_consecutive_duplicates_from_sequence([0, 0, 1, 2, 3, 3, 3, 4, 5])
      [0, 1, 2, 3, 4, 5]

   Return list.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.remove_repetitions( )`` to
      ``seqtools.remove_consecutive_duplicates_from_sequence( )``.
   '''

   result = [ ]

   first_element = False
   for element in sequence:
      if not first_element:
         first_element = True
         #yield element
         result.append(element)
      else:
         if not element == prev_element:
            #yield element
            result.append(element)
      prev_element = element

   return result
