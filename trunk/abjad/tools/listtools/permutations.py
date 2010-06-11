def permutations(l):
   '''Yield all permutations of ``l``.

   ::

      abjad> l = [1, 2, 3]
      abjad> listtools.permutations(l)
      <generator object at 0x118c0d0>
      abjad> list(_)
      [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]

   .. note:: This is a stop-gap for Python 2.5 because the 2.6 \
   implementation of ``itertools`` includes a built-in ``permutations`` \
   function.
   '''

   ## base case
   if len(l) == 1:
      yield(l)
      raise StopIteration

   ## inductive case
   for i in range(len(l)):
      element_slice = l[i:i+1]
      rest_iter = permutations(l[:i] + l[i+1:])
      for rest in rest_iter:
         yield(element_slice + rest)

   raise StopIteration
