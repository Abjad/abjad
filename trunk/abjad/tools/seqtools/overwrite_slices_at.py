## TODO Implement optional period keyword.
## TODO Read anchor_index and length values cyclically.
def overwrite_slices_at(sequence, pairs):
   '''Overwrite `sequence` slices at `pairs`::

      seqtools.overwrite_slices_at(range(10), [(0, 3), (5, 3)])
      [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]

   Set `pairs` to a list of ``(anchor_index, length)`` pairs.

   Return new list.
   '''

   result = sequence[:]

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
