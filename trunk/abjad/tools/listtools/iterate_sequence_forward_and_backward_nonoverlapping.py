def iterate_sequence_forward_and_backward_nonoverlapping(iterable):
   '''.. versionadded:: 1.1.2

   Yield elements in `iterable` first forward and then backward,
   with first and last elements repeated. ::

      abjad> list(listtools.iterate_sequence_forward_and_backward_nonoverlapping([1, 2, 3, 4, 5]))
      [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]

   .. versionchanged:: 1.1.2
      renamed ``listtools.forward_and_backward_nonoverlapping( )`` to
      ``listtools.iterate_sequence_forward_and_backward_nonoverlapping( )``.
   '''

   iterable_copy = [ ]
   for x in iterable:
      yield x
      iterable_copy.append(x)
   for x in reversed(iterable_copy):
      yield x   
