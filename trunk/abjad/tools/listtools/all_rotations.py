from abjad.tools.listtools.rotate import rotate

def all_rotations(lst):
   '''.. versionadded:: 1.1.2

   Yield all rotations of list `lst`. ::

      abjad> listtools.all_rotations(range(5))
      <generator object at 0x89f0d8c>
      abjad> list(_)
      [[0, 1, 2, 3, 4], 
       [1, 2, 3, 4, 0], 
       [2, 3, 4, 0, 1], 
       [3, 4, 0, 1, 2], 
       [4, 0, 1, 2, 3]]
   '''
   for i in range(len(lst)):
      yield rotate(lst, -i)
   
