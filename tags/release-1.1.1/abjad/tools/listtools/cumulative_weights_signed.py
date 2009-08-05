from abjad.tools import mathtools


def cumulative_weights_signed(l):
   '''Yield signed weights of the cumulative elements in *l*

   .. note:: This function returns a generator.

   ::

      abjad> l = [1, -2, -3, 4, -5, -6, 7, -8, -9, 10]
      abjad> list(listtools.cumulative_weights_signed(l))
      [1, -3, -6, 10, -15, -21, 28, -36, -45, 55]

   ::

      abjad> l = [-1, -2, -3, -4, -5, 6, 7, 8, 9, 10]
      abjad> list(listtools.cumulative_weights_signed(l))
      [-1, -3, -6, -10, -15, 21, 28, 36, 45, 55]

   ::

      abjad> l = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      abjad> list(listtools.cumulative_weights_signed(l))
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

   ::

      abjad> l = [1, 2, 3, 4, 5, 0, 0, 0, 0, 0]
      abjad> list(listtools.cumulative_weights_signed(l))
      [1, 3, 6, 10, 15, 15, 15, 15, 15, 15]

   ::

      abjad> l = [-1, -2, -3, -4, -5, 0, 0, 0, 0, 0]
      abjad> list(listtools.cumulative_weights_signed(l))
      [-1, -3, -6, -10, -15, -15, -15, -15, -15, -15]

   .. note:: For cumulative (unsigned) weights use \
      ``listtools.cumulative_sums([abs(x) for x in l])``.

   Raise :exc:`TypeError` when *l* is not a list::

      abjad> list(listtools.cumulative_weights_signed('foo'))
      TypeError
   '''

   if not isinstance(l, list):
      raise TypeError

   for x in l:
      try:
         next = abs(prev) + abs(x)
         prev_sign = mathtools.sign(prev)
      except NameError:
         next = abs(x)
         prev_sign = 0
      sign_x = mathtools.sign(x)
      if sign_x == -1:
         next *= sign_x
      elif sign_x == 0:
         next *= prev_sign
      yield next
      prev = next

   raise StopIteration
