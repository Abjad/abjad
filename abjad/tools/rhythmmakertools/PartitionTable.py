# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.datastructuretools import TypedOrderedDict


class PartitionTable(TypedOrderedDict):
    r'''Partition table.

    ..  container:: example

        **Example 1.** Partitions integers roughly ``1:1`` (restricted to
        assignable values) with larger half on left:

        ::

            >>> table = rhythmmakertools.PartitionTable([
            ...     (2, [1, 1]),
            ...     (3, [2, 1]),
            ...     (5, [3, 2]),
            ...     (7, [4, 3]),
            ...     ])

        ::

            >>> print(format(table))
            rhythmmakertools.PartitionTable(
                [
                    (
                        2,
                        mathtools.Ratio(1, 1),
                        ),
                    (
                        3,
                        mathtools.Ratio(2, 1),
                        ),
                    (
                        5,
                        mathtools.Ratio(3, 2),
                        ),
                    (
                        7,
                        mathtools.Ratio(4, 3),
                        ),
                    ]
                )

    ..  container:: example

        **Example 2.** Partitions integers roughly ``1:1`` (restricted to
        assignable values) with larger half on right:

        ::

            >>> table = rhythmmakertools.PartitionTable([
            ...     (2, [1, 1]),
            ...     (3, [1, 2]),
            ...     (5, [2, 3]),
            ...     (7, [3, 4]),
            ...     ])

        ::

            >>> print(format(table))
            rhythmmakertools.PartitionTable(
                [
                    (
                        2,
                        mathtools.Ratio(1, 1),
                        ),
                    (
                        3,
                        mathtools.Ratio(1, 2),
                        ),
                    (
                        5,
                        mathtools.Ratio(2, 3),
                        ),
                    (
                        7,
                        mathtools.Ratio(3, 4),
                        ),
                    ]
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE METHODS ###

    def _item_coercer(self, item):
        item = mathtools.Ratio(item)
        return item