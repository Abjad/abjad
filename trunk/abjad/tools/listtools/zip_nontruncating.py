def zip_nontruncating(*lists):
   '''Zip but do not truncate like built-in Python :func:`zip`.

   Lengths of the tuples returned may differ but will always be 
   greater than or equal to ``1``. ::

      abjad> listtools.zip_nontruncating([1, 2, 3, 4], [11, 12, 13])     
      [(1, 11), (2, 12), (3, 13), (4,)]

   ::

      abjad> listtools.zip_nontruncating([1, 2, 3], [11, 12, 13, 14])
      [(1, 11), (2, 12), (3, 13), (14,)]

   Arbitrary numbers of lists are supported. ::

      abjad> k = range(100, 103)
      abjad> l = range(200, 201)
      abjad> m = range(300, 303)
      abjad> n = range(400, 408)
      abjad> listtools.zip_nontruncating(k, l, m, n)
      [(100, 200, 300, 400), (101, 301, 401), (102, 302, 402), (403,), (404,), (405,), (406,), (407,)]
   '''

   result = [ ]

   max_length = max([len(l) for l in lists])
   for i in range(max_length):
      part = [ ]
      for l in lists:
         try:
            part.append(l[i])
         except IndexError:
            pass
      result.append(tuple(part))

   return result
