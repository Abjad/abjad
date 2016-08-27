# -*- coding: utf-8 -*-
from abjad.tools import durationtools
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
            abjad.rhythmmakertools.PartitionTable(
                [
                    (
                        2,
                        mathtools.NonreducedRatio((1, 1)),
                        ),
                    (
                        3,
                        mathtools.NonreducedRatio((2, 1)),
                        ),
                    (
                        5,
                        mathtools.NonreducedRatio((3, 2)),
                        ),
                    (
                        7,
                        mathtools.NonreducedRatio((4, 3)),
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
            abjad.rhythmmakertools.PartitionTable(
                [
                    (
                        2,
                        mathtools.NonreducedRatio((1, 1)),
                        ),
                    (
                        3,
                        mathtools.NonreducedRatio((1, 2)),
                        ),
                    (
                        5,
                        mathtools.NonreducedRatio((2, 3)),
                        ),
                    (
                        7,
                        mathtools.NonreducedRatio((3, 4)),
                        ),
                    ]
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _item_coercer(self, item):
        item = mathtools.NonreducedRatio(item)
        return item

    ### PUBLIC METHODS ###

    def respell_division(self, division):
        r'''Respells `division` according to partition table.

        ..  container:: example

            **Example 1.** Respells divisions according to table:

            ::

                >>> table = rhythmmakertools.PartitionTable([
                ...     (2, [1, 1]),
                ...     (3, [2, 1]),
                ...     (5, [3, 2]),
                ...     (7, [4, 3]),
                ...     ])

            ::

                >>> for numerator in range(1, 15):
                ...     division = mathtools.NonreducedFraction(numerator, 4)
                ...     result = table.respell_division(division)
                ...     print((division, result))
                ...
                (NonreducedFraction(1, 4), [NonreducedFraction(1, 4)])
                (NonreducedFraction(2, 4), [NonreducedFraction(1, 4), NonreducedFraction(1, 4)])
                (NonreducedFraction(3, 4), [NonreducedFraction(2, 4), NonreducedFraction(1, 4)])
                (NonreducedFraction(4, 4), [NonreducedFraction(2, 4), NonreducedFraction(2, 4)])
                (NonreducedFraction(5, 4), [NonreducedFraction(3, 4), NonreducedFraction(2, 4)])
                (NonreducedFraction(6, 4), [NonreducedFraction(4, 4), NonreducedFraction(2, 4)])
                (NonreducedFraction(7, 4), [NonreducedFraction(4, 4), NonreducedFraction(3, 4)])
                (NonreducedFraction(8, 4), [NonreducedFraction(4, 4), NonreducedFraction(4, 4)])
                (NonreducedFraction(9, 4), [NonreducedFraction(6, 4), NonreducedFraction(3, 4)])
                (NonreducedFraction(10, 4), [NonreducedFraction(6, 4), NonreducedFraction(4, 4)])
                (NonreducedFraction(11, 4), [NonreducedFraction(11, 4)])
                (NonreducedFraction(12, 4), [NonreducedFraction(8, 4), NonreducedFraction(4, 4)])
                (NonreducedFraction(13, 4), [NonreducedFraction(13, 4)])
                (NonreducedFraction(14, 4), [NonreducedFraction(8, 4), NonreducedFraction(6, 4)])

        ..  container:: example

            **Example 2.** Respells divisions according to another table:

            ::

                >>> table = rhythmmakertools.PartitionTable([
                ...     (5, [1, 3, 1]),
                ...     (7, [1, 2, 4]),
                ...     ])

            ::

                >>> for numerator in range(1, 15):
                ...     division = mathtools.NonreducedFraction(numerator, 4)
                ...     result = table.respell_division(division)
                ...     print((division, result))
                ...
                (NonreducedFraction(1, 4), [NonreducedFraction(1, 4)])
                (NonreducedFraction(2, 4), [NonreducedFraction(2, 4)])
                (NonreducedFraction(3, 4), [NonreducedFraction(3, 4)])
                (NonreducedFraction(4, 4), [NonreducedFraction(4, 4)])
                (NonreducedFraction(5, 4), [NonreducedFraction(1, 4), NonreducedFraction(3, 4), NonreducedFraction(1, 4)])
                (NonreducedFraction(6, 4), [NonreducedFraction(6, 4)])
                (NonreducedFraction(7, 4), [NonreducedFraction(1, 4), NonreducedFraction(2, 4), NonreducedFraction(4, 4)])
                (NonreducedFraction(8, 4), [NonreducedFraction(8, 4)])
                (NonreducedFraction(9, 4), [NonreducedFraction(9, 4)])
                (NonreducedFraction(10, 4), [NonreducedFraction(2, 4), NonreducedFraction(6, 4), NonreducedFraction(2, 4)])
                (NonreducedFraction(11, 4), [NonreducedFraction(11, 4)])
                (NonreducedFraction(12, 4), [NonreducedFraction(12, 4)])
                (NonreducedFraction(13, 4), [NonreducedFraction(13, 4)])
                (NonreducedFraction(14, 4), [NonreducedFraction(2, 4), NonreducedFraction(4, 4), NonreducedFraction(8, 4)])

        Returns list of new divisions.
        '''
        division = mathtools.NonreducedFraction(division)
        result = [division]
        divisors = mathtools.divisors(division.numerator)
        for numerator, ratio in reversed(list(self.items())):
            if numerator in divisors:
                result = [division * _ for _ in ratio.multipliers]
                break
        result = [mathtools.NonreducedFraction(_) for _ in result]
        return result
