def phasor(lst, step=1, start=0, length='inf'):
   '''Iterate cyclically over *lst*.

   - *lst* is a ``list`` of arbitrary objects to iterate through.
   - *step* jump size and direction across list.
   - *start* : the index of *lst* where the function begins iterating.
   - *length* number of elements to return. if ``'inf'``, returns
      infinitely.
     
   The function returns a generator.

   Examples:

   ::

      abjad> l = [1, 2, 3, 4, 5, 6, 7]

   ::

      abjad> g = listtools.phasor(l)
      abjad> for i in range(20):
      ...     print g.next( ),
      ... 
      1 2 3 4 5 6 7 1 2 3 4 5 6 7 1 2 3 4 5 6

   ::

      abjad> listtools.phasor(l, 2, length = 20)
      <generator object at 0x8264acc>
      abjad> list(_)
      [1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4]
 
   ::

      abjad> listtools.phasor(l, 2, 3, length = 20)
      <generator object at 0x8264acc>
      abjad> list(_)
      [4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7, 2, 4, 6, 1, 3, 5, 7]

   ::

      abjad> listtools.phasor(l, -2, 5, length = 20)
      <generator object at 0x8264acc>
      abjad> list(_)
      [6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3, 1, 6, 4, 2, 7, 5, 3]

   '''

   assert isinstance(lst, list)
   assert isinstance(step, int)
   assert isinstance(start, int)
   if isinstance(length, str):
      assert length == 'inf'
   else:
      assert isinstance(length, int)

   phase = start
   if length == 'inf':
      while True:
         yield lst[phase]
         phase = (phase + step) % len(lst)
   else:
      for i in range(length):
         yield lst[phase]
         phase = (phase + step) % len(lst)

