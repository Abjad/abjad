def get_cyclic(sequence, start, stop):
   '''Iterate `sequence` cyclically from `start` to `stop`::

      abjad> list(seqtools.get_cyclic(range(20), 18, 10))
      [18, 19, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
   
   Return generator of references to `sequence` elements.
   '''

   len_sequence = len(sequence)
   cur_index = start
   cyclic_stop = stop % len_sequence
   while True:
      cyclic_cur_index = cur_index % len_sequence
      if cyclic_cur_index == cyclic_stop:
         return
      else:
         yield sequence[cyclic_cur_index]
         cur_index += 1
