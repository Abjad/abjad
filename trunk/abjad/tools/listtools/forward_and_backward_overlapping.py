def forward_and_backward_overlapping(iterable):
   '''.. versionadded:: 1.1.2

   Yield elements in `iterable` first forward and then backward,
   with first and last elements appearing only once. ::

      abjad> list(listtools.forward_and_backward_overlapping([1, 2, 3, 4, 5]))
      [1, 2, 3, 4, 5, 4, 3, 2]
   '''

   iterable_copy = [ ]
   for x in iterable:
      yield x
      iterable_copy.append(x)
   for x in reversed(iterable_copy[1:-1]):
      yield x
