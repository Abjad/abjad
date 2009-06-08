def get_cyclic(l, start_index, stop_index):
   '''Iterate ``l`` from ``start_index % len(l)`` to ``stop_index % len(l)``.

   *  When ``start_index <= stop_index`` behave as the usual \
      ``l[start_index:stop_index]``.
   *  When ``stop_index < start_index`` wrap around the end of ``l``.

   ::

      abjad> l
      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

   ::

      abjad> listtools.get_cyclic(l, 18, 10)
      <generator object at 0x117daf8>
      abjad> list(_)
      [18, 19, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
   
   ::

      abjad> listtools.get_cyclic(l, 10, 18)
      <generator object at 0x117daf8>
      abjad> list(_)
      [10, 11, 12, 13, 14, 15, 16, 17]

   ::

      abjad> listtools.get_cyclic(l, 10, 10)
      <generator object at 0x117daf8>
      abjad> list(_)
      []

   Note that the output of this function is a generator.

   .. todo:: Optimize the slow implementation given here.'''

   len_l = len(l)
   cur_index = start_index
   cyclic_stop_index = stop_index % len_l

   while True:
      cyclic_cur_index = cur_index % len_l
      if cyclic_cur_index == cyclic_stop_index:
         return
      else:
         yield l[cyclic_cur_index]
         cur_index += 1
