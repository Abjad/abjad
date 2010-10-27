def overwrite_slices_at(l, pairs):
   '''Overwrite slices in *l* according to *pairs*.

   *  *pairs* must be a list ``(anchor_index, length)`` pairs. \
      The function then copies the value of ``l[anchor_index]`` \
      over ``l[anchor_index + 1]``, ``l[anchor_index + 2]``, ...,
      ``l[anchor_index + length - 1]``.

   Return new list.

   ::

      abjad> l = range(10)
      seqtools.overwrite_slices_at(l, [(0, 3), (5, 3)])
      [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]

   ::

      abjad> l = range(10)
      seqtools.overwrite_slices_at(l, [(0, 99)])
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

   .. todo:: Implement optional ``period`` keyword.

   .. todo:: Read *anchor_index* and *length* values cyclically.
   '''

   result = l[:]

   for anchor_index, length in pairs:
      anchor = result[anchor_index]
      start = anchor_index + 1
      stop = start + length - 1
      for i in range(start, stop):
         try:
            result[i] = anchor
         except IndexError:
            break
      
   return result
