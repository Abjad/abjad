from __future__ import division


def zip_sequences_cyclically(*sequences):
    '''.. versionadded:: 1.1

    Zip `sequences` cyclically::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.zip_sequences_cyclically([1, 2, 3], ['a', 'b'])
        [(1, 'a'), (2, 'b'), (3, 'a')]

    .. versionadded:: 1.1
        Arbitrary number of input sequences now allowed.

    ::

        abjad> sequencetools.zip_sequences_cyclically([10, 11, 12], [20, 21], [30, 31, 32, 33])
        [(10, 20, 30), (11, 21, 31), (12, 20, 32), (10, 21, 33)]

    Cycle over the elements of the sequences of shorter length.

    Return list of length equal to sequence of greatest length in `sequences`.

    .. versionchanged:: 2.0
        renamed ``sequencetools.zip_cyclic()`` to
        ``sequencetools.zip_sequences_cyclically()``.
    '''

    # make sure sequences are, in fact, all sequences
    new_sequences = []
    for sequence in sequences:
        if not isinstance(sequence, (list, tuple)):
            new_sequences.append([sequence])
        else:
            new_sequences.append(sequence)

    # find length of longest sequence
    max_length = max([len(x) for x in new_sequences])

    # produce list of tuples
    result = []
    for i in range(max_length):
        part = [x[i % len(x)] for x in new_sequences]
        result.append(tuple(part))

    # return result
    return result
