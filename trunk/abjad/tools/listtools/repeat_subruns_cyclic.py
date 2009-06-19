from abjad.component.component import _Component


def repeat_subruns_cyclic(l, indicators):
   '''Repeat subruns in `l` according to `indicators`.
   The `indicators` input parameter must be a list of 
   zero or more ``(start, length, repetitions)`` triples.
   The function copies ``l[start:start+length]`` and inserts 
   ``repetitions`` times for each ``(start, length, repetitions)`` indicator 
   in `indicators`.

   To insert ``10`` repetitions of ``l[:2]`` at ``l[2:2]``::
   
      abjad> listtools.repeat_subruns_cyclic(range(20), [(0, 2, 10)])
      [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 
      2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

   To insert ``5`` repetitions of ``l[10:12]`` at ``l[12:12]`` and then
   insert ``5`` repetitions of ``l[:2]`` at ``l[2:2]``::

      abjad> listtools.repeat_subruns_cyclic(l, [(0, 2, 5), (10, 2, 5)])
      [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
      10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
      
   To insert ``2`` repetitions of ``[18, 19, 0, 1]`` at ``l[2:2]``::

      abjad> listtools.repeat_subruns_cyclic(l, [(18, 4, 2)])
      [0, 1, 18, 19, 0, 1, 18, 19, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

   To insert ``2`` repetitions of ``[18, 19, 0, 1, 2, 3, 4]`` at ``l[4:4]``::

      abjad> listtools.repeat_subruns_cyclic(l, [(18, 8, 2)])
      [0, 1, 2, 3, 4, 5, 18, 19, 0, 1, 2, 3, 4, 5, 18, 19, 0, 1, 2, 3, 4, 
      5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

   .. todo:: Reimplement this function to return a generator.'''

   assert isinstance(l, list)
   assert all([not isinstance(x, _Component) for x in l])
   assert isinstance(indicators, list)
   assert all([len(x) == 3 for x in indicators])

   len_l = len(l)
   instructions = [ ]

   for start, length, repetitions in indicators:
      new_slice = [ ]
      stop = start + length
      for i in range(start, stop):
         new_slice.append(l[i % len_l])
      index = stop % len_l
      instruction = (index, new_slice, repetitions)
      instructions.append(instruction)

   result = l[:]

   for index, new_slice, repetitions in reversed(sorted(instructions)):
      for i in range(repetitions):
         result[index:index] = new_slice
         
   return result
