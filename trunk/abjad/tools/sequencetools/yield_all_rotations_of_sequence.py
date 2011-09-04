from abjad.tools.sequencetools.rotate_sequence import rotate_sequence


def yield_all_rotations_of_sequence(sequence, n = 1):
    '''.. versionadded:: 2.0

    Yield all `n`-rotations of `sequence` up to identity::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> list(sequencetools.yield_all_rotations_of_sequence([1, 2, 3, 4], -1))
        [[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2], [4, 1, 2, 3]]

    Return generator of `sequence` objects.
    '''

    len_sequence = len(sequence)
    total_rotations_yielded = 0

    yield rotate_sequence(sequence, 0)
    total_rotations_yielded += 1

    index = n
    while True:
        rotation = rotate_sequence(sequence, index)
        if len_sequence <= total_rotations_yielded:
            break
        elif rotation == sequence:
            break
        else:
            yield rotation
            total_rotations_yielded += 1
        index += n
