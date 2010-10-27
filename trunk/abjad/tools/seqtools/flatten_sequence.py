def flatten_sequence(l, ltypes = (list, tuple), depth = -1):
   '''Flatten nested lists `l`. Return a 0-depth list or tuple.
   Set optional `depth` keyword set to positive integer.
   Keyword controls depth to which the function operates.
   Based on Mike C. Fletcher's flatten. ::

      abjad> t = [1, [2, 3, [4]], 5, [6, 7, [8]]]
      abjad> seqtools.flatten_sequence(t)
      [1, 2, 3, 4, 5, 6, 7, 8]

   ::

      abjad> seqtools.flatten_sequence(t, depth = 0)
      [1, [2, 3, [4]], 5, [6, 7, [8]]]

   ::

      abjad> seqtools.flatten_sequence(t, depth = 1)
      [1, 2, 3, [4], 5, 6, 7, [8]]

   ::

      abjad> seqtools.flatten_sequence(t, depth = 2)
      [1, 2, 3, 4, 5, 6, 7, 8]

   .. versionchanged:: 1.1.2
      renamed ``seqtools.flatten( )`` to
      ``seqtools.flatten_sequence( )``.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.flatten_iterable( )`` to
      ``seqtools.flatten_sequence( )``.
   '''

   assert isinstance(l, ltypes)
   ltype = type(l)
   return ltype(_flatten_helper(l, ltypes, depth))


# Creates an iterator that can generate a flattened list, 
# descending down into child elements to a depth given in the
# argments.
# Note: depth < 0 is effectively equivalent to "infinity"
def _flatten_helper(lst, ltypes, depth):
   if not isinstance(lst, ltypes):
      yield lst
   elif depth==0:
      for i in lst:
         yield i
   else:
      for i in lst:
         # Flatten an iterable by one level
         for j in _flatten_helper(i, ltypes, depth-1):
            yield j
