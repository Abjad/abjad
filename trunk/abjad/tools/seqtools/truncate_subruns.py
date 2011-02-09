from fractions import Fraction


def truncate_subruns(sequence):
   '''Truncate subruns of like elements in `sequence` to length ``1``::

      abjad> seqtools.truncate_subruns([1, 1, 2, 3, 3, 3, 9, 4, 4, 4])
      [1, 2, 3, 9, 4]

   Return empty list when `sequence` is empty::

      abjad> seqtools.truncate_subruns([ ])
      [ ]

   Raise type error when `sequence` is not a list::

      abjad> seqtools.truncate_subruns(1)
      TypeError

   Return new list.
   '''

   if not isinstance(sequence, list):
      raise TypeError

   assert all([isinstance(x, (int, float, Fraction)) for x in sequence])

   result = [ ]

   if sequence:
      result.append(sequence[0])
      for element in sequence[1:]:
         if not element == result[-1]:
            result.append(element)

   return result
