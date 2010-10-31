from abjad.tools import mathtools
import itertools


def group_sequence_elements_by_sign(sequence, sign = [-1, 0, 1]):
   '''Group `sequence` elements by sign.

   Behavior of `sign`:

   *  When ``-1`` in ``sign``, group negative elements.
   *  When ``0`` in ``sign``, group ``0`` elements.
   *  When ``1`` in ``sign``, group positive elements.
   *  Default to ``[-1, 0, 1]``.

   ::

      abjad> sequence = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(sequence)
      abjad> generator
      <generator object at 0x118bf30>
      abjad> list(generator)
      [[0, 0], [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(sequence, sign = [-1])
      abjad> generator
      <generator object at 0x118f1e8>
      abjad> list(generator)
      [0, 0, [-1, -1], 2, 3, [-5], 1, 2, 5, [-5, -6]]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(sequence, sign = [0])
      abjad> generator
      <generator object at 0x118f288>
      abjad> list(generator)
      [[0, 0], -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(sequence, sign = [1])
      abjad> generator
      <generator object at 0x118f2d8>
      abjad> list(generator)
      [0, 0, -1, -1, [2, 3], -5, [1, 2, 5], -5, -6]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(sequence, sign = [-1, 0])
      abjad> generator
      <generator object at 0x118f350>
      abjad> list(generator)
      [[0, 0], [-1, -1], 2, 3, [-5], 1, 2, 5, [-5, -6]]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(sequence, sign = [-1, 1])
      abjad> generator
      <generator object at 0x118f418>
      abjad> list(generator)
      [0, 0, [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(sequence, sign = [0, 1])
      abjad> generator
      <generator object at 0x118f508>
      abjad> list(generator)
      [[0, 0], -1, -1, [2, 3], -5, [1, 2, 5], -5, -6]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(sequence, sign = [-1, 0, 1])
      abjad> generator
      <generator object at 0x118bf30>
      abjad> list(generator)
      [[0, 0], [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

   Return list of tuples of `sequence` element references.

   .. versionchanged:: 1.1.2
      renamed ``listtools.group_by_sign( )`` to
      ``seqtools.group_sequence_elements_by_sign( )``.
   '''

   result = [ ]
   g = itertools.groupby(sequence, mathtools.sign)
   for cur_sign, group in g:
      if cur_sign in sign:
         result.append(tuple(group))
      else:
         for x in group:
            result.append(x)
   return result 
