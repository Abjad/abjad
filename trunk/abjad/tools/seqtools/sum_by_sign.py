from abjad.tools import mathtools
import itertools


def sum_by_sign(l, sign = [-1, 0, 1]):
   '''Sum elements in *l* by *sign*.

   Behavior of *sign*:

   .. |element| unicode:: U+2208 .. set membership

   *  When ``-1`` |element| *sign*, sum consecutive negative elements.
   *  When ``0`` |element| *sign*, sum consecutive ``0`` elements.
   *  When ``1`` |element| *sign*, sum consecutive positive elements.
   *  Default to ``[-1, 0, 1]``.

   Examples::

      abjad> l = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

   ::
   
      abjad> generator = seqtools.sum_by_sign(l)
      abjad> generator
      <generator object at 0x118bf30>
      abjad> list(generator)
      [0, -2, 5, -5, 8, -11]

   ::
   
      abjad> generator = seqtools.sum_by_sign(l, sign = [-1])
      abjad> generator
      <generator object at 0x118f1e8>
      abjad> list(generator)
      [0, 0, -2, 2, 3, -5, 1, 2, 5, -11]

   ::
   
      abjad> generator = seqtools.sum_by_sign(l, sign = [0])
      abjad> generator
      <generator object at 0x118f288>
      abjad> list(generator)
      [0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

   ::
   
      abjad> generator = seqtools.sum_by_sign(l, sign = [1])
      abjad> generator
      <generator object at 0x118f2d8>
      abjad> list(generator)
      [0, 0, -1, -1, 5, -5, 8, -5, -6]

   ::
   
      abjad> generator = seqtools.sum_by_sign(l, sign = [-1, 0])
      abjad> generator
      <generator object at 0x118f350>
      abjad> list(generator)
      [0, -2, 2, 3, -5, 1, 2, 5, -11]

   ::
   
      abjad> generator = seqtools.sum_by_sign(l, sign = [-1, 1])
      abjad> generator
      <generator object at 0x118f418>
      abjad> list(generator)
      [0, 0, -2, 5, -5, 8, -11]

   ::
   
      abjad> generator = seqtools.sum_by_sign(l, sign = [0, 1])
      abjad> generator
      <generator object at 0x118f508>
      abjad> list(generator)
      [0, -1, -1, 5, -5, 8, -5, -6]

   ::
   
      abjad> generator = seqtools.sum_by_sign(l, sign = [-1, 0, 1])
      abjad> generator
      <generator object at 0x118bf30>
      abjad> list(generator)
      [0, -2, 5, -5, 8, -11]
   '''

   generator = itertools.groupby(l, mathtools.sign)
   for cur_sign, group in generator:
      if cur_sign in sign:
         yield sum(group)
      else:
         for x in group:
            yield x
