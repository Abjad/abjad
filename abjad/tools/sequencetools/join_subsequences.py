# -*- coding: utf-8 -*-
import collections
from abjad.tools import mathtools


def join_subsequences(sequence):
    '''Join subsequences in `sequence`.

    ..  container:: example

        **Example 1.** Joins tuples:

        ::

            >>> tuples = [(1, 2, 3), (), (4, 5), (), (6,)]
            >>> sequencetools.join_subsequences(tuples)
            (1, 2, 3, 4, 5, 6)

    ..  container:: example

        **Example 2.** Joins lists:

        ::

            >>> lists = [[1, 2, 3], [], [4, 5], [], [6]]
            >>> sequencetools.join_subsequences(lists)
            [1, 2, 3, 4, 5, 6]

    Returns new object of `sequence` type.
    '''

    if not isinstance(sequence, collections.Sequence):
        message = 'must be sequence: {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    return mathtools.cumulative_sums(sequence, start=None)[-1]
