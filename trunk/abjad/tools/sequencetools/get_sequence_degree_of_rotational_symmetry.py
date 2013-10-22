# -*- encoding: utf-8 -*-


def get_sequence_degree_of_rotational_symmetry(sequence):
    '''Change `sequence` to degree of rotational symmetry:

    ::

        >>> sequencetools.get_sequence_degree_of_rotational_symmetry([1, 2, 3, 4, 5, 6])
        1

    ::

        >>> sequencetools.get_sequence_degree_of_rotational_symmetry([1, 2, 3, 1, 2, 3])
        2

    ::

        >>> sequencetools.get_sequence_degree_of_rotational_symmetry([1, 2, 1, 2, 1, 2])
        3

    ::

        >>> sequencetools.get_sequence_degree_of_rotational_symmetry([1, 1, 1, 1, 1, 1])
        6

    Returns positive integer.
    '''

    degree_of_rotational_symmetry = 0
    for index in range(len(sequence)):
        rotation = sequence[index:] + sequence[:index]
        if rotation == sequence:
            degree_of_rotational_symmetry += 1
    return degree_of_rotational_symmetry
