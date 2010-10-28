def sequence_to_degree_of_rotational_symmetry(sequence):
   '''.. versionadded:: 1.1.2

   Change `sequence` to degree of rotational symmetry::

      abjad> seqtools.sequence_to_degree_of_rotational_symmetry([1, 2, 3, 4, 5, 6])
      1

   ::

      abjad> seqtools.sequence_to_degree_of_rotational_symmetry([1, 2, 3, 1, 2, 3])
      2

   ::

      abjad> seqtools.sequence_to_degree_of_rotational_symmetry([1, 2, 1, 2, 1, 2])
      3

   ::

      abjad> seqtools.sequence_to_degree_of_rotational_symmetry([1, 1, 1, 1, 1, 1])
      6

   Return positive integer.
   '''

   degree_of_rotational_symmetry = 0
   for index in range(len(sequence)):
      rotation = sequence[index:] + sequence[:index]
      if rotation == sequence:
         degree_of_rotational_symmetry += 1
   return degree_of_rotational_symmetry
