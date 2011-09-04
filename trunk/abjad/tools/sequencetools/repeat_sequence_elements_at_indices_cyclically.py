def repeat_sequence_elements_at_indices_cyclically(sequence, cycle_token, total):
    '''.. versionadded:: 2.0

    Repeat `sequence` elements at indices specified by `cycle_token` to `total` length::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.repeat_sequence_elements_at_indices_cyclically(range(10), (5, [1, 2]), 3)
        [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, [6, 6, 6], [7, 7, 7], 8, 9]

    The `cycle_token` may be a sieve::

        abjad> from abjad.tools import sievetools

    ::

        abjad> sieve = sievetools.cycle_tokens_to_sieve((5, [1, 2]))
        abjad> sequencetools.repeat_sequence_elements_at_indices_cyclically(range(10), sieve, 3)
        [0, [1, 1, 1], [2, 2, 2], 3, 4, 5, [6, 6, 6], [7, 7, 7], 8, 9]

    Return list.
    '''
    from abjad.tools import sievetools

    sieve = sievetools.cycle_tokens_to_sieve(cycle_token)
    list_sequence = list(sequence)
    indices = sieve.get_congruent_bases(len(list_sequence))

    result = []

    for i, element in enumerate(sequence):
        if i in indices:
            #yield [element] * total
            result.append(total * [element])
        else:
            #yield element
            result.append(element)

    return result
