from abjad.tools.listtools.rotate import rotate

def yield_all_rotations_of_iterable(lst):
   '''.. versionadded:: 1.1.2

   Yield all rotations of list `lst`. ::

      abjad> listtools.yield_all_rotations_of_iterable(range(5))
      <generator object at 0x89f0d8c>
      abjad> list(_)
      [[0, 1, 2, 3, 4], 
       [1, 2, 3, 4, 0], 
       [2, 3, 4, 0, 1], 
       [3, 4, 0, 1, 2], 
       [4, 0, 1, 2, 3]]

   .. versionchanged:: 1.1.2
      renamed ``listtools.all_rotations( )`` to
      ``listtools.yield_all_rotations_of_iterable( )``.
   '''
   for i in range(len(lst)):
      yield rotate(lst, -i)
   
