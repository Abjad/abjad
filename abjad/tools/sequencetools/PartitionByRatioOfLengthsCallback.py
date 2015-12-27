# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadValueObject


class PartitionByRatioOfLengthsCallback(AbjadValueObject):
    r'''A partition-by-ratio-of-lengths callback.

    ..  container:: example

        **Example 1.** Partitions sequence by ``1:1:1`` ratio:

        ::

            >>> callback = sequencetools.partition_sequence_by_ratio_of_lengths(
            ...     None,
            ...     mathtools.Ratio((1, 1, 1)),
            ...     )
            >>> sequence = list(range(10))
            >>> callback(sequence)
            [[0, 1, 2], [3, 4, 5, 6], [7, 8, 9]]

        Returns list of lists.

    ..  container:: example

        **Example 2.** Partitions sequence by ``1:1:2`` ratio:

        ::

            >>> callback = sequencetools.partition_sequence_by_ratio_of_lengths(
            ...     None,
            ...     mathtools.Ratio((1, 1, 2)),
            ...     )
            >>> sequence = tuple(range(10))
            >>> callback(sequence)
            [(0, 1, 2), (3, 4), (5, 6, 7, 8, 9)]

        Returns list of tuples.

    Returns list of objects equal in type to input argument.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'

    __slots__ = (
        '__callback',
        '_ratio',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        ratio=None,
        ):
        from abjad.tools import sequencetools
        self.__callback = sequencetools.partition_sequence_by_ratio_of_lengths
        self._ratio = ratio

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls callback on `expr`.
        '''
        result = self.__callback(
            expr, 
            ratio=self.ratio
            )
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def ratio(self):
        r'''Gets ratio of callback.

        Returns ratio or none.
        '''
        return self._ratio