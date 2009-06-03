from abjad.rational.rational import Rational


def repeat_to_length(l, length):
   '''Repeat list ``l`` to ``length``.
   
   * ``l`` must be an iterable of one or more numbers.
   * ``length`` must be a nonnegative integer.

   ::

      abjad> l = range(5)
      abjad> listtools.repeat_to_length(l, 11)
      [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]

   When ``length < len(l)`` return only the first \
   ``length`` elements of ``l``.

   ::

      abjad> l = range(5)
      abjad> listtools.repeat_to_length(l, 3)
      [0, 1, 2]

   When ``length`` is ``0`` return an empty list.

   ::

      abjad> l = range(5)
      abjad> listtools.repeat_to_length(l, 0)
      [ ]'''

   assert isinstance(length, (int, long)) and 0 <= length
   assert all([isinstance(x, (int, float, long, Rational)) for x in l])

   result = [ ]

   for i in range(length):
      result.append(l[i % len(l)])

   return result
