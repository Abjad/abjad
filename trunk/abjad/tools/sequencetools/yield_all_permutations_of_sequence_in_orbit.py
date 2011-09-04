from abjad.tools.sequencetools.is_permutation import is_permutation
from abjad.tools.sequencetools.permute_sequence import permute_sequence


def yield_all_permutations_of_sequence_in_orbit(sequence, permutation):
    '''.. versionadded:: 2.0

    Yield all permutations of `sequence` in orbit of `permutation` in lex order::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> list(sequencetools.yield_all_permutations_of_sequence_in_orbit((1, 2, 3, 4), [1, 2, 3, 0]))
        [(1, 2, 3, 4), (2, 3, 4, 1), (3, 4, 1, 2), (4, 1, 2, 3)]

    Return generator of `sequence` objects.
    '''

    if not is_permutation(permutation, len(sequence)):
        args = (str(permutation), len(sequence))
        raise TypeError('"%s" must be permutation of length %s.' % args)

    # return identity first #
    next_permutation = permute_sequence(sequence, range(len(sequence)))
    yield next_permutation

    # then return remaining permutations in orbit of permutation #
    while True:
        next_permutation = permute_sequence(next_permutation, permutation)
        if next_permutation == sequence:
            break
        else:
            yield next_permutation
