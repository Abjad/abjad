# -*- encoding: utf-8 -*-
from abjad.tools import mathtools


def join_subsequences(sequence):
    '''Join subsequences in `sequence`.

    ::

        >>> sequencetools.join_subsequences([(1, 2, 3), (), (4, 5), (), (6,)])
        (1, 2, 3, 4, 5, 6)

    Returns newly constructed object of subsequence type.
    '''

    return mathtools.cumulative_sums(sequence, start=None)[-1]
