# TODO: make function return a list of two-element multisets.
def yield_all_unordered_pairs_of_sequence(sequence):
    '''.. versionadded:: 2.0

    Yield all unordered pairs of `sequence`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> list(sequencetools.yield_all_unordered_pairs_of_sequence([1, 2, 3, 4]))
        [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]

    Yield all unordered pairs of length-``1`` `sequence`::

        abjad> list(sequencetools.yield_all_unordered_pairs_of_sequence([1]))
        []

    Yield all unordered pairs of empty `sequence`::

        abjad> list(sequencetools.yield_all_unordered_pairs_of_sequence([]))
        []

    Yield all unordered pairs of `sequence` with duplicate elements::

        abjad> list(sequencetools.yield_all_unordered_pairs_of_sequence([1, 1, 1]))
        [(1, 1), (1, 1), (1, 1)]

    Pairs are tuples instead of sets to accommodate duplicate `sequence` elements.

    Return generator.
    '''

    #result = []
    sequence_copy = list(sequence)

    for i, x in enumerate(sequence_copy):
        for y in sequence_copy[i+1:]:
            pair = (x, y)
            #result.append(pair)
            yield pair

    #return result
