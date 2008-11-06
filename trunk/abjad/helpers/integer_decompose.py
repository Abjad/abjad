from abjad.helpers.binary import _binary


def _integer_decompose(n):
   '''Return big-ending tuple of n.

      Example:

      >>> for i in range(10, 20):
      ...     print i, _integer_decompose(i)
      ... 
      10 (8, 2)
      11 (8, 3)
      12 (12,)
      13 (12, 1)
      14 (14,)
      15 (15,)
      16 (16,)
      17 (16, 1)
      18 (16, 2)
      19 (16, 3)
   '''

   assert isinstance(n, int)

   if n == 0:
      return (0, )
   
   result = [ ]
   prev_empty = True
   binary_n = _binary(n)
   binary_length = len(binary_n)

   for i, x in enumerate(binary_n):
      if x == '1':
         place_value = 2 ** (binary_length - i - 1)
         if prev_empty:
            result.append(place_value)
         else:
            result[-1] += place_value
         prev_empty = False
      else:
         prev_empty = True

   return tuple(result)
