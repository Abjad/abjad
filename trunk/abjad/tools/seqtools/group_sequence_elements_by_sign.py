from abjad.tools import mathtools
import itertools


def group_sequence_elements_by_sign(l, sign = [-1, 0, 1]):
   '''Group elements in *l* by sign.

   .. |element| unicode:: U+2208 .. set membership

   Behavior of *sign*:

   *  When ``-1`` |element| ``sign``, group negative elements.
   *  When ``0`` |element| ``sign``, group ``0`` elements.
   *  When ``1`` |element| ``sign``, group positive elements.
   *  Default to ``[-1, 0, 1]``.

   Examples::

      abjad> l = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(l)
      abjad> generator
      <generator object at 0x118bf30>
      abjad> list(generator)
      [[0, 0], [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(l, sign = [-1])
      abjad> generator
      <generator object at 0x118f1e8>
      abjad> list(generator)
      [0, 0, [-1, -1], 2, 3, [-5], 1, 2, 5, [-5, -6]]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(l, sign = [0])
      abjad> generator
      <generator object at 0x118f288>
      abjad> list(generator)
      [[0, 0], -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(l, sign = [1])
      abjad> generator
      <generator object at 0x118f2d8>
      abjad> list(generator)
      [0, 0, -1, -1, [2, 3], -5, [1, 2, 5], -5, -6]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(l, sign = [-1, 0])
      abjad> generator
      <generator object at 0x118f350>
      abjad> list(generator)
      [[0, 0], [-1, -1], 2, 3, [-5], 1, 2, 5, [-5, -6]]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(l, sign = [-1, 1])
      abjad> generator
      <generator object at 0x118f418>
      abjad> list(generator)
      [0, 0, [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(l, sign = [0, 1])
      abjad> generator
      <generator object at 0x118f508>
      abjad> list(generator)
      [[0, 0], -1, -1, [2, 3], -5, [1, 2, 5], -5, -6]

   ::
   
      abjad> generator = seqtools.group_sequence_elements_by_sign(l, sign = [-1, 0, 1])
      abjad> generator
      <generator object at 0x118bf30>
      abjad> list(generator)
      [[0, 0], [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

   .. versionchanged:: 1.1.2
      renamed ``seqtools.group_by_sign( )`` to
      ``seqtools.group_sequence_elements_by_sign( )``.
   '''

   g = itertools.groupby(l, mathtools.sign)
   for cur_sign, group in g:
      if cur_sign in sign:
         yield list(group)
      else:
         for x in group:
            yield x
