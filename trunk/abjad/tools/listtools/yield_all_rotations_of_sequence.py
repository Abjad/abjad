from abjad.tools.listtools.rotate_sequence import rotate_sequence


def yield_all_rotations_of_sequence(sequence):
   '''.. versionadded:: 1.1.2

   Yield all rotations of `sequence`::

      abjad> for rotation in listtools.yield_all_rotations_of_sequence(range(5)):
      ...   rotation
      [0, 1, 2, 3, 4] 
      [1, 2, 3, 4, 0] 
      [2, 3, 4, 0, 1] 
      [3, 4, 0, 1, 2] 
      [4, 0, 1, 2, 3]

   Return generator of newly created `sequence` slices.

   .. versionchanged:: 1.1.2
      renamed ``listtools.all_rotations( )`` to
      ``listtools.yield_all_rotations_of_sequence( )``.
   '''

   for i in range(len(sequence)):
      yield rotate_sequence(sequence, -i)
