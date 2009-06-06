def zip_nontruncating(*lists):
   '''Zip but do not truncate like built-in Python :func:`zip`.

   ::

      abjad> listtools.zip_nontruncating([1, 2, 3, 4], [11, 12, 13])     
      [(1, 11), (2, 12), (3, 13), (4,)]

   ::

      abjad> listtools.zip_nontruncating([1, 2, 3], [11, 12, 13, 14])
      [(1, 11), (2, 12), (3, 13), (14,)]'''

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
