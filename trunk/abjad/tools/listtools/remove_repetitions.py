def remove_repetitions(iterable):
   '''.. versionadded:: 1.1.2

   Yield elements in `iterable` with consecutive
   like elements removed. ::

      abjad> list(listtools.remove_repetitions([0, 0, 1, 2, 3, 3, 3, 4, 5]))
      [0, 1, 2, 3, 4, 5]
   '''

   first_element = False
   for element in iterable:
      if not first_element:
         first_element = True
         yield element
      else:
         if not element == prev_element:
            yield element
      prev_element = element
