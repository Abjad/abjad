from abjad.tools.datastructuretools.OrderedDict import OrderedDict


class PartitionTable(OrderedDict):
    """
    Partition table.

    ..  container:: example

        Partitions integers roughly ``1:1`` (restricted to assignable values)
        with larger half on left:

        >>> table = abjad.rmakers.PartitionTable([
        ...     (2, [1, 1]),
        ...     (3, [2, 1]),
        ...     (5, [3, 2]),
        ...     (7, [4, 3]),
        ...     ])

        >>> abjad.f(table)
        abjad.rmakers.PartitionTable(
            [
                (
                    2,
                    abjad.NonreducedRatio((1, 1)),
                    ),
                (
                    3,
                    abjad.NonreducedRatio((2, 1)),
                    ),
                (
                    5,
                    abjad.NonreducedRatio((3, 2)),
                    ),
                (
                    7,
                    abjad.NonreducedRatio((4, 3)),
                    ),
                ]
            )

    ..  container:: example

        Partitions integers roughly ``1:1`` (restricted to assignable values)
        with larger half on right:

        >>> table = abjad.rmakers.PartitionTable([
        ...     (2, [1, 1]),
        ...     (3, [1, 2]),
        ...     (5, [2, 3]),
        ...     (7, [3, 4]),
        ...     ])

        >>> abjad.f(table)
        abjad.rmakers.PartitionTable(
            [
                (
                    2,
                    abjad.NonreducedRatio((1, 1)),
                    ),
                (
                    3,
                    abjad.NonreducedRatio((1, 2)),
                    ),
                (
                    5,
                    abjad.NonreducedRatio((2, 3)),
                    ),
                (
                    7,
                    abjad.NonreducedRatio((3, 4)),
                    ),
                ]
            )

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = ()

    _publish_storage_format = True

    ### PRIVATE METHODS ###

    @staticmethod
    def _item_coercer(item):
        import abjad
        item = abjad.NonreducedRatio(item)
        return item

    ### PUBLIC METHODS ###

    def respell_division(self, division):
        """
        Respells ``division`` according to partition table.

        ..  container:: example

            Respells divisions according to table:

            >>> table = abjad.rmakers.PartitionTable([
            ...     (2, [1, 1]),
            ...     (3, [2, 1]),
            ...     (5, [3, 2]),
            ...     (7, [4, 3]),
            ...     ])

            >>> for numerator in range(1, 15):
            ...     division = abjad.NonreducedFraction(numerator, 4)
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

            Respells divisions according to another table:

            >>> table = abjad.rmakers.PartitionTable([
            ...     (5, [1, 3, 1]),
            ...     (7, [1, 2, 4]),
            ...     ])

            >>> for numerator in range(1, 15):
            ...     division = abjad.NonreducedFraction(numerator, 4)
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
        """
        import abjad
        division = abjad.NonreducedFraction(division)
        result = [division]
        divisors = abjad.mathtools.divisors(division.numerator)
        for numerator, ratio in reversed(list(self.items())):
            if numerator in divisors:
                result = [division * _ for _ in ratio.multipliers]
                break
        result = [abjad.NonreducedFraction(_) for _ in result]
        return result
