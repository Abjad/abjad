def trivial_float_to_int(n):
   '''.. versionadded:: 1.1.2

   Cast float `n` to int when ``float(n) == int(n)``. ::

      abjad> mathtools.trivial_float_to_int(7.0)
      7

   Otherwise, return `n` unchanged. ::

      abjad> mathtools.trivial_float_to_int(7.5)
      7.5
   '''

   int_n = int(n)
   if int_n == n:
      return int_n
   return n
