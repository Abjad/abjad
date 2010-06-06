from abjad.tools.mathtools.sign import sign


def partition_integer_into_units(n):
   '''Partition integer *n* into *n* equal parts.

   Partition positive *n* into parts all equal to ``1``::

      abjad> mathtools.partition_integer_into_units(6)
      [1, 1, 1, 1, 1, 1]

   Partition negative *n* into parts all equal to ``-1``::

      abjad> mathtools.partition_integer_into_units(-5)
      [-1, -1, -1, -1, -1]

   Return empty list when *n* is ``0``::

      abjad> mathtools.partition_integer_into_units(0)
      []

   Raise :exc:`TypeError` on noninteger *n*::

      abjad> mathtools.partition_integer_into_units(7.5)
      TypeError
   '''

   return [sign(n) * 1] * abs(n)
