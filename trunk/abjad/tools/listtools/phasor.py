import itertools


def phasor(iterable, step=1, start=0, length='inf'):
   '''Yield elements in `iterable` cyclically according to `step`,
   `start` and `length`.

   - `iterable`: any iterable.
   - `step`: jump size and direction across list.
   - `start`: the index of `iterable` where the function begins iterating.
   - `length`: number of elements to return. If ``'inf'``, returns infinitely.
     
   Examples. ::

      abjad> list(listtools.phasor(l, length = 20))
      [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6]

   ::

      abjad> list(listtools.phasor(l, 2, length = 20))
      [1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4]
 
   ::

      abjad> list(listtools.phasor(l, 2, 3, length = 20))
      [4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7]

   ::

      abjad> list(listtools.phasor(l, -2, 5, length = 20))
      [6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3]

   .. versionchanged:: 1.1.2
      allows generator input.

   ::

      abjad> generator = listtools._generator(1, 8)
      abjad> list(listtools.phasor(generator, -2, 5, length = 20))
      [6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3]
   '''

   #assert isinstance(iterable, list)
   assert isinstance(step, int)
   assert isinstance(start, int)
   if isinstance(length, str):
      assert length == 'inf'
   else:
      assert isinstance(length, int)

#   phase = start
#   if length == 'inf':
#      while True:
#         yield iterable[phase]
#         phase = (phase + step) % len(iterable)
#   else:
#      for i in range(length):
#         yield iterable[phase]
#         phase = (phase + step) % len(iterable)

   ## itertools.islice( ) does not handle negative step.
   ## so we divided iterable into two halves from start index.
   ## then we reverse those two halves.
   ## then we recombined the halves and pass positive step.
   if step < 0:
      step = abs(step)
      list_iterable = list(iterable)
      left, right = reversed(list_iterable[:start-1]), reversed(list_iterable[start-1:])
      iterable = itertools.chain(left, right)

   ## iterate and yield
   total = 0
   for x in itertools.islice(itertools.cycle(iterable), start, None, step):
      yield x
      total += 1
      if not length == 'inf':
         if total == length:
            raise StopIteration
