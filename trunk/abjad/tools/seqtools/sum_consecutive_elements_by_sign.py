from abjad.tools import mathtools
import itertools


def sum_consecutive_elements_by_sign(sequence, sign = [-1, 0, 1]):
   '''Sum consecutive `sequence` elements by `sign`::

      abjad> l = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

   ::
   
      abjad> list(seqtools.sum_consecutive_elements_by_sign(l))
      [0, -2, 5, -5, 8, -11]

   ::
   
      abjad> list(seqtools.sum_consecutive_elements_by_sign(l, sign = [-1]))
      [0, 0, -2, 2, 3, -5, 1, 2, 5, -11]

   ::
   
      abjad> list(seqtools.sum_consecutive_elements_by_sign(l, sign = [0]))
      [0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

   ::
   
      abjad> list(seqtools.sum_consecutive_elements_by_sign(l, sign = [1]))
      [0, 0, -1, -1, 5, -5, 8, -5, -6]

   ::
   
      abjad> list(seqtools.sum_consecutive_elements_by_sign(l, sign = [-1, 0]))
      [0, -2, 2, 3, -5, 1, 2, 5, -11]

   ::
   
      abjad> list(seqtools.sum_consecutive_elements_by_sign(l, sign = [-1, 1]))
      [0, 0, -2, 5, -5, 8, -11]

   ::
   
      abjad> list(seqtools.sum_consecutive_elements_by_sign(l, sign = [0, 1]))
      [0, -1, -1, 5, -5, 8, -5, -6]

   ::
   
      abjad> list(seqtools.sum_consecutive_elements_by_sign(l, sign = [-1, 0, 1]))
      [0, -2, 5, -5, 8, -11]

   .. |element| unicode:: U+2208 .. set membership

   When ``-1`` |element| `sign`, sum consecutive negative elements.

   When ``0`` |element| `sign`, sum consecutive ``0`` elements.

   When ``1`` |element| `sign`, sum consecutive positive elements.

   Return generator.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.sum_by_sign( )`` to
      ``seqtools.sum_consecutive_elements_by_sign( )``.
   '''

   generator = itertools.groupby(sequence, mathtools.sign)
   for cur_sign, group in generator:
      if cur_sign in sign:
         yield sum(group)
      else:
         for x in group:
            yield x
