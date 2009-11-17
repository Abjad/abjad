def all_restricted_growth_functions_of_length(n):
   '''.. versionadded:: 1.1.2

   Yield all restricted growth functions of length `n` in lex order. ::

      abjad> for rgf in listtools.all_restricted_growth_functions_of_length(4):
      ...     rgf
      ... 
      [1, 1, 1, 1]
      [1, 1, 1, 2]
      [1, 1, 2, 1]
      [1, 1, 2, 2]
      [1, 1, 2, 3]
      [1, 2, 1, 1]
      [1, 2, 1, 2]
      [1, 2, 1, 3]
      [1, 2, 2, 1]
      [1, 2, 2, 2]
      [1, 2, 2, 3]
      [1, 2, 3, 1]
      [1, 2, 3, 2]
      [1, 2, 3, 3]
      [1, 2, 3, 4]
   '''

   if not isinstance(n, int):
      raise TypeError('must be integer.')
   if not 0 < n:
      raise ValueError('must be positive.')

   last_rgf = range(1, n + 1)

   rgf = [1] * n
   yield rgf
   
   while not rgf == last_rgf:
      for i, x in enumerate(reversed(rgf)):
         if x < max(rgf[:-(i+1)]) + 1:
            first_part = rgf[:-(i+1)]
            increased_part = [rgf[-(i+1)] + 1]
            trailing_ones = [1] * i
            rgf = first_part + increased_part + trailing_ones
            yield rgf
            break
