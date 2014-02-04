# -*- encoding: utf-8 -*-


def yield_all_rotations_of_sequence(sequence, n=1):
    '''Yields all `n`-rotations of `sequence`.

    ::

        >>> list(sequencetools.yield_all_rotations_of_sequence([1, 2, 3, 4], -1))
        [[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2], [4, 1, 2, 3]]

    Yields rotations up to but not including identity.

    Returns generator of `sequence` objects.
    '''
    from abjad.tools import sequencetools

    len_sequence = len(sequence)
    total_rotations_yielded = 0

    yield sequencetools.rotate_sequence(sequence, 0)
    total_rotations_yielded += 1

    index = n
    while True:
        rotation = sequencetools.rotate_sequence(sequence, index)
        if len_sequence <= total_rotations_yielded:
            break
        elif rotation == sequence:
            break
        else:
            yield rotation
            total_rotations_yielded += 1
        index += n
