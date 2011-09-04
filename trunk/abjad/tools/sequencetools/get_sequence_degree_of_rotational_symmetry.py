def get_sequence_degree_of_rotational_symmetry(sequence):
    '''.. versionadded:: 2.0

    Change `sequence` to degree of rotational symmetry::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.get_sequence_degree_of_rotational_symmetry([1, 2, 3, 4, 5, 6])
        1

    ::

        abjad> sequencetools.get_sequence_degree_of_rotational_symmetry([1, 2, 3, 1, 2, 3])
        2

    ::

        abjad> sequencetools.get_sequence_degree_of_rotational_symmetry([1, 2, 1, 2, 1, 2])
        3

    ::

        abjad> sequencetools.get_sequence_degree_of_rotational_symmetry([1, 1, 1, 1, 1, 1])
        6

    Return positive integer.
    '''

    degree_of_rotational_symmetry = 0
    for index in range(len(sequence)):
        rotation = sequence[index:] + sequence[:index]
        if rotation == sequence:
            degree_of_rotational_symmetry += 1
    return degree_of_rotational_symmetry
