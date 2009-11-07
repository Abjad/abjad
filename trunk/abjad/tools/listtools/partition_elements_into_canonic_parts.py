from abjad.tools import mathtools


def partition_elements_into_canonic_parts(l, direction = 'big-endian'):
   '''Partition elements in `l` into canonic parts according to `direction`.

   ::

      abjad> l = range(10)
      abjad> listtools.partition_elements_into_canonic_parts(l)
      [(0,), (1,), (2,), (3,), (4,), (4, 1), (6,), (7,), (8,), (8, 1)]

   ::

      abjad> l = range(10)
      abjad> listtools.partition_elements_into_canonic_parts(l, direction = 'little-endian')
      [(0,), (1,), (2,), (3,), (4,), (1, 4), (6,), (7,), (8,), (1, 8)]

   Raise :exc:`TypeError` when `l` is not a list. ::

      abjad> listtools.partition_elements_into_canonic_parts('foo')
      TypeError

   Raise :exc:`ValueError` on noninteger elements in `l`. ::

      abjad> listtools.partition_elements_into_canonic_parts([Rational(1, 2), Rational(1, 2)])
      ValueError
   '''

   if not isinstance(l, list):
      raise TypeError

   if not all([isinstance(x, (int, long)) for x in l]):
      raise ValueError

   result = [ ]

   for x in l: 
      result.append(mathtools.partition_integer_into_canonic_parts(
         x, direction = direction))
   
   return result
