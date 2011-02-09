from abjad.tools import mathtools
import itertools


def sum_consecutive_elements_by_sign(sequence, sign = [-1, 0, 1]):
   '''Sum consecutive `sequence` elements by `sign`::

      abjad> sequence = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

   ::
   
      abjad> seqtools.sum_consecutive_elements_by_sign(sequence)
      [0, -2, 5, -5, 8, -11]

   ::
   
      abjad> seqtools.sum_consecutive_elements_by_sign(sequence, sign = [-1])
      [0, 0, -2, 2, 3, -5, 1, 2, 5, -11]

   ::
   
      abjad> seqtools.sum_consecutive_elements_by_sign(sequence, sign = [0])
      [0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

   ::
   
      abjad> seqtools.sum_consecutive_elements_by_sign(sequence, sign = [1])
      [0, 0, -1, -1, 5, -5, 8, -5, -6]

   ::
   
      abjad> seqtools.sum_consecutive_elements_by_sign(sequence, sign = [-1, 0])
      [0, -2, 2, 3, -5, 1, 2, 5, -11]

   ::
   
      abjad> seqtools.sum_consecutive_elements_by_sign(sequence, sign = [-1, 1])
      [0, 0, -2, 5, -5, 8, -11]

   ::
   
      abjad> sequence(seqtools.sum_consecutive_elements_by_sign(sequence, sign = [0, 1])
      [0, -1, -1, 5, -5, 8, -5, -6]

   ::
   
      abjad> seqtools.sum_consecutive_elements_by_sign(sequence, sign = [-1, 0, 1])
      [0, -2, 5, -5, 8, -11]

   .. |element| unicode:: U+2208 .. set membership

   When ``-1`` |element| `sign`, sum consecutive negative elements.

   When ``0`` |element| `sign`, sum consecutive ``0`` elements.

   When ``1`` |element| `sign`, sum consecutive positive elements.

   Return list.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.sum_by_sign( )`` to
      ``seqtools.sum_consecutive_elements_by_sign( )``.
   '''

   result = [ ]

   generator = itertools.groupby(sequence, mathtools.sign)
   for cur_sign, group in generator:
      if cur_sign in sign:
         #yield sum(group)
         result.append(sum(group))
      else:
         for x in group:
            #yield x
            result.append(x)

   return result
