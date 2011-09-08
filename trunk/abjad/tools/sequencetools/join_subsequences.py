from abjad.tools import mathtools


def join_subsequences(sequence):
    '''.. versionadded:: 2.4

    Join subsequences in `sequence`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.join_subsequences([(1, 2, 3), (), (4, 5), (), (6,)])
        (1, 2, 3, 4, 5, 6)

    Return newly constructed object of subsequence type.
    '''

    return mathtools.cumulative_sums(sequence)[-1]
