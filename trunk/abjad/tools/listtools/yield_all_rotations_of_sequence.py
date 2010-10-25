from abjad.tools.listtools.rotate_iterable import rotate_iterable

def yield_all_rotations_of_sequence(lst):
   '''.. versionadded:: 1.1.2

   Yield all rotations of list `lst`. ::

      abjad> listtools.yield_all_rotations_of_sequence(range(5))
      <generator object at 0x89f0d8c>
      abjad> list(_)
      [[0, 1, 2, 3, 4], 
       [1, 2, 3, 4, 0], 
       [2, 3, 4, 0, 1], 
       [3, 4, 0, 1, 2], 
       [4, 0, 1, 2, 3]]

   .. versionchanged:: 1.1.2
      renamed ``listtools.all_rotations( )`` to
      ``listtools.yield_all_rotations_of_sequence( )``.

   .. versionchanged:: 1.1.2
      renamed ``listtools.yield_all_rotations_of_iterable( )`` to
      ``listtools.yield_all_rotations_of_sequence( )``.
   '''
   for i in range(len(lst)):
      yield rotate_iterable(lst, -i)
   
