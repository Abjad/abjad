from abjad.tools.seqtools.rotate_sequence import rotate_sequence


def yield_all_rotations_of_sequence(sequence, n = 1):
   '''.. versionadded:: 1.1.2

   Yield all `n`-rotations of `sequence` up to identity::

      abjad> list(seqtools.yield_all_rotations_of_sequence([1, 2, 3, 4], -1))
      [[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2], [4, 1, 2, 3]]

   Return generator of `sequence` types.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.all_rotations( )`` to
      ``seqtools.yield_all_rotations_of_sequence( )``.
   '''

   yield rotate_sequence(sequence, 0)

   index = n
   while True:
      rotation = rotate_sequence(sequence, index)
      if rotation == sequence:
         break
      else:
         yield rotation
      index += n
