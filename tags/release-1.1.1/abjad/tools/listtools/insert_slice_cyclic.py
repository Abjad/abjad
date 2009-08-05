def insert_slice_cyclic(l, s, overhang = (0, 0)):
   '''Insert a copy of the elements of *s* between each of the 
   elements of *l*. Read *overhang* to determine whether to insert
   a copy of the elements of s before the first element of *l*
   or after the last element of *l*.

   * When ``overhang[0] == 1`` insert a copy of the elements of *s* \
      before the first element of *l*.
   * When ``overhang[-1] == 1`` insert a copy of the elements of *s* \
      after the last element of *l*.

   Examples:

   ::
  
      >>> l = [0, 1, 2, 3, 4]
      >>> s = ['A', 'B']

   ::

      >>> listtools.insert_slice_cyclic(l, s)
      [0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4]

   ::

      >>> listtools.insert_slice_cyclic(l, s, overhang = (0, 1))
      [0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4, 'A', 'B']

   ::

      >>> listtools.insert_slice_cyclic(l, s, overhang = (1, 0))
      ['A', 'B', 0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4]

   ::

      >>> listtools.insert_slice_cyclic(l, s, overhang = (1, 1))
      ['A', 'B', 0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4, 'A', 'B']'''

   result = [ ]

   if overhang[0] == 1:
      result.extend(s)

   for element in l[:-1]:
      result.append(element)
      result.extend(s)

   result.append(l[-1])

   if overhang[-1] == 1:
      result.extend(s)

   return result
